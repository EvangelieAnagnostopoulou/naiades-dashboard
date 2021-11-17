import requests

from furl import furl


class OrionError(ValueError):

    def __init__(self, error, *args, **kwargs):
        self.error = error

        super(*args, **kwargs).__init__()


class OrionClient(object):
    endpoint = '5.53.108.182:1026'
    history_endpoint = '5.53.108.182/time-series-api'
    service = None

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

    def get(self, resource, params=None, source=endpoint):
        # get everything as key/value pair by default
        if not params:
            params = {}

        if source == self.endpoint:
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
    service = 'alicante'
