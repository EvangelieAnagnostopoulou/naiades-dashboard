import pytz
import tqdm

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from context_manager_api import ContextManagerAPIClient
from context_manager_api.orion import OrionError
from naiades_dashboard.models import MeterInfo, Consumption


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
            "lastN": 10000,
        })

        # filter out devices with missing id
        devices = [
            device
            for device in devices
            if device.get("id") and device.get("serialNumber")
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

    def process_data(self, data, device, latest_consumption=None):
        # get device params for consumption records
        params = {
            'meter_number_id': device["serialNumber"],
            'activity': self.meter_infos_idx[device["serialNumber"]].activity,
        }

        # parse data
        consumptions = []
        timestamps = set()
        for idx, timestamp_str in enumerate(data.get("index", [])):
            # get consumption
            consumption = data["values"][idx]

            # parse timestamp
            # a consumption value for 12:00 should be saved with start time 11:00
            # since the value returned is the consumption measured last 60 minutes
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f'). \
                replace(minute=0, second=0, microsecond=0, tzinfo=pytz.UTC) - timedelta(hours=1)

            # ignore if hour was already processed
            if timestamp in timestamps:
                continue

            timestamps.add(timestamp)

            # avoid inserting duplicates
            if latest_consumption and latest_consumption.date >= timestamp:
                continue

            # add consumption record
            consumptions.append(Consumption.parse_and_create(
                consumption=consumption,
                timestamp=timestamp,
                **params
            ))

        # bulk create
        Consumption.objects.bulk_create(consumptions)

    def pull_latest_data(self, device):
        # get latest consumption for this device
        latest_consumption = Consumption.objects.\
            filter(meter_number=device["serialNumber"]).\
            order_by('-date').\
            first()

        # get data
        try:
            data = self.client.get(
                resource=f'entities/{device["id"]}/attrs/value',
                source=self.client.history_endpoint,
                params={
                    "lastN": 10000,
                },
            )
        except OrionError as e:
            # ignore not found errors for now
            if e.error.get("error") == "Not Found":
                return

            raise

        # process
        self.process_data(data=data, device=device, latest_consumption=latest_consumption)

    def handle(self, *args, **kwargs):
        # initialize client
        self.client = ContextManagerAPIClient()

        # load devices
        devices = self.load_updated_devices()

        # pull new deliveries
        for device in tqdm.tqdm(devices):
            self.pull_latest_data(device=device)
