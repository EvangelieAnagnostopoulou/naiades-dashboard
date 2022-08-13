import random
from datetime import timedelta

import tqdm
from django.contrib.auth.models import User

from django.db.models import *
from naiades_dashboard.lists import *


def rand_range(range):
    return range[0] + random.random() * range[1]


ACTIVITY_SCHOOL = "School"


class MeterInfo(Model):
    meter_number = CharField(max_length=32, primary_key=True)
    activity = CharField(max_length=128)
    description = TextField(blank=True)

    # location
    latitude = DecimalField(max_digits=16, decimal_places=8, db_column="Lat")
    longitude = DecimalField(max_digits=16, decimal_places=8, db_column="Long")
    address = CharField(max_length=128, blank=True, default='')

    # service info
    service_point_id = IntegerField(blank=True, null=True, default=None)
    service_connection_id = IntegerField(blank=True, null=True, default=None)

    # other metadata
    name = CharField(max_length=128, blank=True, default='')

    # size (e.g. number of users for schools)
    size = IntegerField(blank=True, null=True, default=None)

    # show in dashboard?
    in_dashboard = BooleanField(default=False)
    in_dashboard_changed = BooleanField(default=False)

    def to_dict(self):
        return {
            "meter_number": self.meter_number,
            "name": self.name or f'Meter {self.meter_number}',
            "activity": self.activity,
            "latitude": "%.8f" % self.latitude,
            "longitude": "%.8f" % self.longitude,
            "address": self.address,
            "service_point_id": self.service_point_id,
            "service_connection_id": self.service_connection_id,
            "size": self.size,
        }


class BaseConsumption(Model):
    # value
    consumption = DecimalField(max_digits=32, decimal_places=16)

    # timestamp breakdown
    date = DateTimeField(db_index=True)
    year = SmallIntegerField()
    month = SmallIntegerField()
    week = SmallIntegerField()
    day = SmallIntegerField()
    hour = SmallIntegerField()

    # is consumption estimated?
    estimated = BooleanField(default=False)

    class Meta:
        abstract = True


class Consumption(BaseConsumption):
    # related meter number
    meter_number = ForeignKey('naiades_dashboard.MeterInfo', on_delete=CASCADE, related_name='consumptions')

    # check if shown in dashboard
    in_dashboard = BooleanField(default=False)

    @staticmethod
    def get_params_from_timestamp(timestamp):
        return {
            "date": timestamp,
            "year": timestamp.year,
            "week": timestamp.isocalendar()[1],
            "month": timestamp.month,
            "day": timestamp.weekday(),
            "hour": timestamp.hour,
        }

    @staticmethod
    def parse_and_create(meter_info, consumption, timestamp, estimated=False):
        return Consumption(
            meter_number=meter_info,
            consumption=consumption,
            in_dashboard=meter_info.in_dashboard,
            estimated=estimated,
            **Consumption.get_params_from_timestamp(timestamp=timestamp)
        )


class ConsumptionByActivity(BaseConsumption):
    # hourly consumption for specific activity
    activity = CharField(max_length=128)

    class Meta:
        verbose_name = "Consumption by Activity"
        verbose_name_plural = "Consumptions by Activity"
        unique_together = ("date", "hour", "activity", "estimated", )

    @staticmethod
    def _get_diffs(consumptions):
        diffs = {}
        for consumption in consumptions:
            key = (
                consumption.meter_number.activity,
                consumption.date,
                consumption.estimated,
            )

            if key not in diffs:
                diffs[key] = 0

            diffs[key] += consumption.consumption

        return diffs

    @staticmethod
    def update_from_consumptions(consumptions):
        # get diffs for each activity/date/hour
        diffs = ConsumptionByActivity._get_diffs(consumptions=consumptions)

        # apply to db
        for key, consumption_diff in diffs.items():
            activity, timestamp, estimated = key
            obj, _ = ConsumptionByActivity.objects.get_or_create(
                activity=activity,
                estimated=estimated,
                **Consumption.get_params_from_timestamp(timestamp=timestamp),
                defaults={
                    "consumption": 0,
                }
            )
            obj.consumption += consumption_diff
            obj.save()

    @staticmethod
    def update(activity, timestamp, estimated):
        # calculate total
        total = Consumption.objects.filter(
            meter_number__activity=activity,
            date=timestamp,
            estimated=estimated
        ).aggregate(total_consumption=Sum("consumption"))['total_consumption'] or 0

        obj = ConsumptionByActivity.objects.filter(
            activity=activity,
            date=timestamp,
            estimated=estimated,
        ).first()

        if not obj:

            # no object found, null/zero sum
            # no need to create extra record
            if not total:
                return

            # otherwise, create in memory
            obj = ConsumptionByActivity(
                activity=activity,
                estimated=estimated,
                **Consumption.get_params_from_timestamp(timestamp=timestamp),
            )

        # set consumption and update or create
        obj.consumption = total
        obj.save()

    @staticmethod
    def update_for_period(start, end, verbose=False):
        activities = list(set(MeterInfo.objects.values_list('activity', flat=True)))

        timestamp = start
        with tqdm.tqdm(total=(end - start).total_seconds() // 3600, disable=not verbose) as bar:
            while timestamp <= end:
                # show timestamp
                bar.set_description(str(timestamp))

                # generate for all combinations
                for activity in activities:
                    for estimated in [True, False]:
                        ConsumptionByActivity.update(
                            activity=activity,
                            timestamp=timestamp,
                            estimated=estimated,
                        )

                # move to next hour
                timestamp += timedelta(hours=1)

                # update progress
                bar.update(1)


class MeterInfoAccess(Model):
    """
    A user having access to a particular meter, with a specific role
    """
    meter_info = ForeignKey('naiades_dashboard.MeterInfo', on_delete=CASCADE, related_name='accesses')
    user = ForeignKey('auth.User', on_delete=CASCADE, related_name='accesses')
    role = CharField(max_length=16, choices=METER_INFO_ACCESS_ROLES)


class UpdateFile(Model):
    """
    An update file that has been parsed into the system
    """
    created = DateTimeField(auto_now_add=True)
    path = CharField(max_length=512)
    filename = CharField(max_length=256)

    class Meta:
        unique_together = ('path', 'filename')
