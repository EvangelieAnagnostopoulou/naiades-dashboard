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
    latitude = DecimalField(max_digits=16, decimal_places=8, db_column="Lat")
    longitude = DecimalField(max_digits=16, decimal_places=8, db_column="Long")


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

    # is consumption estimated?
    estimated = BooleanField(default=False)

    @staticmethod
    def parse_and_create(meter_number_id, consumption, timestamp, estimated=False):
        return Consumption(
            meter_number_id=meter_number_id,
            consumption=consumption,
            date=timestamp,
            year=timestamp.year,
            week=timestamp.isocalendar()[1],
            month=timestamp.month,
            day=timestamp.weekday(),
            hour=timestamp.hour,
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
