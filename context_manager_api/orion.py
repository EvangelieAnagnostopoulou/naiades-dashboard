import requests

from furl import furl


class OrionError(ValueError):

    def __init__(self, error, *args, **kwargs):
        self.error = error

        super(*args, **kwargs).__init__()

    def __str__(self):
        return str(self.error)


class OrionClient(object):

    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.get("endpoint") or '5.53.108.182:1026'
        self.history_endpoint = kwargs.get("history_endpoint") or '5.53.108.182/time-series-api'
        self.service = kwargs.get("service")

    def get_headers(self, source):
        headers = {}

        headers.update({
            'Fiware-Service': self.service,
        })

        if source == self.history_endpoint:
            headers.update({
                'Fiware-ServicePath': '/',
                'Accept-Encoding': 'gzip, deflate',
            })

        return headers

    @staticmethod
    def handle_error(response):
        # raise generic exception
        raise OrionError(response.json())

    def get(self, resource, params=None, source=None, force_no_options=False):
        source = source or self.endpoint

        # get everything as key/value pair by default
        if not params:
            params = {}

        if source == self.endpoint and not force_no_options:
            params.update({
                "options": "keyValues",
            })

        # list entities
        response = requests.get(
            furl(
                url=f'http://{source}/v2/{resource}',
                args=params
            ).url,
            headers=self.get_headers(source=source)
        )

        # raise exception if response code is in 4xx, 5xx
        if response.status_code >= 400:
            self.handle_error(response)

        # return list
        return response.json()


class ContextManagerAPIClient(OrionClient):

    @staticmethod
    def _add_formatted_alerts(input_alert, item):
        for key in ["short-term", "medium_term", "long_term"]:
            for input_alert_item in (input_alert.get(key) or []):

                # check alert field is not empty
                if not input_alert_item.get("alert"):
                    continue

                # create alert item
                alert_item = {
                    "alert": input_alert_item["alert"],
                    "actions": [],
                }

                # collect possible actions in single field
                for action_prop in ["action", "action1", "action2", "action3"]:
                    if not input_alert_item.get(action_prop):
                        continue

                    alert_item["actions"].append(input_alert_item[action_prop])

                # add alert item to list
                item["alerts"].append(alert_item)

    @staticmethod
    def _formatted_device_alert(input_alert):
        # serial number has to be specified
        if not input_alert.get("device"):
            return None

        # format device alert
        item = {
            "device": {
                "serial_number": input_alert["device"],
                "name": input_alert.get("name") or "",
                "type": input_alert.get("type") or "",
                "location": {
                    "lat": input_alert["location"][1],
                    "lng": input_alert["location"][0],
                } if input_alert.get("location") else None
            },
            "alerts": [],
        }

        # format & add non-empty alerts
        ContextManagerAPIClient._add_formatted_alerts(
            input_alert=input_alert,
            item=item,
        )

        # no need to return an item if no alerts are found
        if not item["alerts"]:
            return None

        return item

    def _get_device_alerts_by_activity(self, activity):
        # get alerts from API
        input_alerts = (
            self.get(
                resource=f"entities/urn:ngsi-ld:Alert:DSS-Alerts-City-{activity}",
                force_no_options=True,
            ).get("value") or {}
        ).get("value")

        # format device alerts
        # and filter out empty ones
        return list(
            filter(
                lambda output_device_alert: output_device_alert,
                map(
                    lambda input_alert: self._formatted_device_alert(input_alert),
                    input_alerts or [],
                )
            )
        )

    def get_device_alerts(self):
        device_alerts = []

        # collect alerts for all activities
        for activity in ["School", "Green", "Sport", "Other"]:
            device_alerts += self._get_device_alerts_by_activity(activity=activity)

        return device_alerts
