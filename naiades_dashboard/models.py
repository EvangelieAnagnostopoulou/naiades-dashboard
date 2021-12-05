import random
from datetime import datetime, timedelta

import tqdm
from dateutil import tz
from django.contrib.auth.models import User

from django.db.models import *
from naiades_dashboard.lists import *


def rand_range(range):
    return range[0] + random.random() * range[1]


class MeterInfo(Model):
    meter_number = CharField(max_length=32, primary_key=True)
    activity = CharField(max_length=128)

    # location
    latitude = DecimalField(max_digits=16, decimal_places=8, db_column="Lat")
    longitude = DecimalField(max_digits=16, decimal_places=8, db_column="Long")
    address = CharField(max_length=128, blank=True, default='')

    # service info
    service_point_id = IntegerField(blank=True, null=True, default=None)
    service_connection_id = IntegerField(blank=True, null=True, default=None)

    # size (e.g. number of users for schools)
    size = IntegerField(blank=True, null=True, default=None)

    def to_dict(self):
        return {
            "meter_number": self.meter_number,
            "name": f'Meter {self.meter_number}',
            "activity": self.activity,
            "latitude": "%.8f" % self.latitude,
            "longitude": "%.8f" % self.longitude,
            "address": self.address,
            "service_point_id": self.service_point_id,
            "service_connection_id": self.service_connection_id,
            "size": self.size,
        }


class Consumption(Model):
    # related meter number
    meter_number = ForeignKey('naiades_dashboard.MeterInfo', on_delete=CASCADE, related_name='consumptions')

    # value
    consumption = DecimalField(max_digits=32, decimal_places=16)

    # timestamp breakdown
    date = DateTimeField()
    year = SmallIntegerField()
    month = SmallIntegerField()
    week = SmallIntegerField()
    day = SmallIntegerField()
    hour = SmallIntegerField()

    # denormalized info about origin to speed up dashboard
    is_school = BooleanField(default=False)

    # is consumption estimated?
    estimated = BooleanField(default=False)

    @staticmethod
    def parse_and_create(meter_number_id, activity, consumption, timestamp, estimated=False):
        return Consumption(
            meter_number_id=meter_number_id,
            consumption=consumption,
            date=timestamp,
            year=timestamp.year,
            week=timestamp.isocalendar()[1],
            month=timestamp.month,
            day=timestamp.weekday(),
            hour=timestamp.hour,
            is_school=activity == 'School',
            estimated=estimated
        )


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
