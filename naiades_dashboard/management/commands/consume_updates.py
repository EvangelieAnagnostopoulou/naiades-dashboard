import pytz
import tqdm

from datetime import datetime

from django.core.management.base import BaseCommand

from context_manager_api import ContextManagerAPIClient
from context_manager_api.orion import OrionError
from naiades_dashboard.models import MeterInfo, Consumption, Indication


class Command(BaseCommand):
    help = 'Consume data updates from context manager api'
    client = None
    meter_infos_idx = None

    def load_updated_devices(self):
        """
        :return: Creates missing MeterInfo objects and returns list of all devices.
        """
        # load existing meter infos
        self.meter_infos_idx = {
            meter_info.meter_number: meter_info
            for meter_info in MeterInfo.objects.all()
        }

        # get from API
        devices = self.client.get(resource="entities", params={
            "type": "Device",
        })

        # filter out devices with missing serial number or id
        devices = [
            device
            for device in devices
            if device.get("serialNumber") and device.get("id")
        ]

        # add missing devices
        new_meter_infos = []
        for device in devices:

            # ignore already existing
            # TODO consider updates
            if device["serialNumber"] in self.meter_infos_idx:
                continue

            # get details
            details = self.client.get(resource=f'entities/{device["id"]}')

            # create meter info
            info = MeterInfo(
                meter_number=device["serialNumber"],
                activity=details["description"],
                latitude=details["location"]["coordinates"][0],
                longitude=details["location"]["coordinates"][1],
            )

            # add to dict
            self.meter_infos_idx.update({
                info.meter_number: info,
            })

            # add to new
            new_meter_infos.append(info)

        # bulk create
        MeterInfo.objects.bulk_create(new_meter_infos)

        # return index with all meter infos
        return devices

    def process_data(self, data, device, indication=None):
        # get device params for consumption records
        params = {
            'meter_number_id': device["serialNumber"],
            'activity': self.meter_infos_idx[device["serialNumber"]].activity,
        }

        # maintain state
        state = {
            "timestamp": None,
            "indication": None,
        }

        # parse data
        consumptions = []
        for idx, timestamp_str in reversed(list(enumerate(data.get("index", [])))):
            # get indication
            indication = data["values"][idx]

            # parse timestamp
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f'). \
                replace(tzinfo=pytz.UTC)

            # check if hour changed
            if state["timestamp"] and state["timestamp"].hour != timestamp.hour:
                consumptions.append(Consumption.parse_and_create(
                    consumption=indication - state["indication"],
                    timestamp=datetime(),
                    **params
                ))

            # break condition
            if latest_consumption and latest_consumption.date > timestamp:
                break

            # add consumption record
            consumptions.append(Consumption.parse_and_create(
                consumption=consumption,
                timestamp=timestamp,
                **params
            ))

        # bulk create
        Consumption.objects.bulk_create(consumptions)

    def pull_latest_data(self, device):
        # get indication for this device
        indication = Indication.objects.\
            filter(meter_number=device["serialNumber"]).\
            first()

        # get data
        try:
            data = self.client.get(
                resource=f'entities/{device["id"]}/attrs/value',
                params={
                    "lastN": 10000,
                },
                source=self.client.history_endpoint
            )
        except OrionError as e:
            # ignore not found errors for now
            if e.error.get("error") == "Not Found":
                return

            raise

        # process
        self.process_data(data=data, device=device, indication=indication)

    def handle(self, *args, **kwargs):
        # initialize client
        self.client = ContextManagerAPIClient()

        # load devices
        devices = self.load_updated_devices()

        # pull new deliveries
        for device in tqdm.tqdm(devices):
            self.pull_latest_data(device=device)
