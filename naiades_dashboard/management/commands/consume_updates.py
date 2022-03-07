import copy
import pytz
import tqdm

from datetime import datetime

from django.core.management.base import BaseCommand

from context_manager_api import ContextManagerAPIClient
from context_manager_api.orion import OrionError
from naiades_dashboard.managers.users import MeterUserManager
from naiades_dashboard.models import MeterInfo, Consumption, ACTIVITY_SCHOOL


class Command(BaseCommand):
    help = 'Consume data updates from context manager api'
    client = None
    meter_infos_idx = None
    user_manager = None
    date_format = '%Y-%m-%dT%H:%M:%S.%f'

    def _parse_timestamp_str(self, timestamp_str):
        return datetime.\
            strptime(timestamp_str, self.date_format).\
            replace(tzinfo=pytz.utc)

    @staticmethod
    def _add_results(response, new_results):
        # list of results
        if type(new_results) == list:

            if not response.get("results"):
                response["results"] = []

            response["results"] += new_results

            return len(new_results)

        # dict of index/values lists
        props = ["index", "values"]
        if not response.get("results"):
            response["results"] = {
                prop: []
                for prop in props
            }

        for prop in props:
            response["results"][prop] += new_results[prop]

        return len(new_results[props[0]])

    def _load_all(self, resource, source, params, page_size):
        response = {}

        offset = 0
        limit = page_size
        while True:
            # prepare request params
            page_params = copy.deepcopy(params)
            page_params.update({
                "offset": offset,
                "limit": limit,
            })

            # get from API
            new_results = self.client.get(
                resource=resource,
                source=source,
                params=page_params
            )

            # add to response
            size = self._add_results(response=response, new_results=new_results)

            # break condition
            if size < page_size:
                break

            # move to next page
            offset += page_size
            limit += page_size

        return response["results"]

    def _load_devices(self):
        # request all from api
        devices = self._load_all(
            resource="entities",
            source=self.client.endpoint,
            params={
                "type": "Device"
            },
            page_size=1000
        )

        # filter out devices with missing id
        # as well as accumulative measurements
        return [
            device
            for device in devices
            if device.get("id") and device.get("serialNumber") and (not device["serialNumber"].endswith("-Accum"))
        ]

    @staticmethod
    def get_activity_type(description):
        desc_lower = (description or "").lower()

        # primary school, high school, reformatory institution are all types of school
        if "school" in desc_lower or "reformatory" in desc_lower:
            return ACTIVITY_SCHOOL

        return description

    @staticmethod
    def _perform_in_dashboard_change(meter_info):
        # update `Consumption` entries
        Consumption.objects.\
            filter(meter_info_id=meter_info.meter_number).\
            update(in_dashboard=meter_info.in_dashboard)

        # changes reflected to `Consumption` model
        meter_info.in_dashboard_changed = False

    def load_updated_devices(self):
        """
        :return: Creates missing MeterInfo objects and returns list of all devices.
        """
        # load existing meter infos
        self.meter_infos_idx = {
            meter_info.meter_number: meter_info
            for meter_info in MeterInfo.objects.all()
        }

        # load all devices from API
        devices = self._load_devices()

        # start user manager
        user_manager = MeterUserManager()

        # add missing devices
        for device in tqdm.tqdm(devices, desc="Updating devices", unit=" devices"):

            # check if exists
            exists = device["serialNumber"] in self.meter_infos_idx

            # get details
            details = self.client.get(resource=f'entities/{device["id"]}')

            # get activity type
            activity = self.get_activity_type(description=details["description"])

            # create meter info
            info = MeterInfo(
                meter_number=device["serialNumber"],
                activity=activity,
                description=details["description"],
                latitude=details["location"]["coordinates"][0],
                longitude=details["location"]["coordinates"][1],
                name=(details.get("name") or "")[:128],
                size=details.get("numberOfUsers"),
            )

            # create or updated
            if exists:
                info.save(update_fields=["latitude", "longitude", "size", "activity", "description"])
            else:
                info.save()
                self.meter_infos_idx.update({
                    info.meter_number: info,
                })

                # create users
                if info.activity == ACTIVITY_SCHOOL:
                    user_manager.create_users(meter_info=info)

            # change data based on in_dashboard prop
            if info.in_dashboard_changed:
                self._perform_in_dashboard_change(meter_info=info)

        # return index with all meter infos
        return devices

    def process_data(self, data, device, latest_consumption=None):
        # get meter info
        meter_info = self.meter_infos_idx[device["serialNumber"]]

        # parse data
        consumptions = []
        for idx, timestamp_str in enumerate(data.get("index", [])):
            # get consumption
            consumption = data["values"][idx]

            # parse timestamp
            timestamp = self._parse_timestamp_str(timestamp_str)

            # avoid inserting duplicates
            if latest_consumption and latest_consumption.date >= timestamp:
                continue

            # add consumption record
            consumptions.append(Consumption.parse_and_create(
                meter_info=meter_info,
                consumption=consumption,
                timestamp=timestamp,
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
            params = {
                "aggrMethod": "sum",
                "aggrPeriod": "hour",
            }

            # only retrieve after latest
            if latest_consumption:
                params.update({
                    "fromDate": latest_consumption.date.strftime(self.date_format)
                })

            # get all consumptions
            data = self._load_all(
                resource=f'entities/{device["id"]}/attrs/value',
                source=self.client.history_endpoint,
                params=params,
                page_size=10000,
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
        for device in tqdm.tqdm(devices, desc="Retrieving consumptions...", unit=" devices"):
            self.pull_latest_data(device=device)
