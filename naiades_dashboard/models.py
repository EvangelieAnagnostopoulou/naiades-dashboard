import random
from datetime import datetime, timedelta

import tqdm
from dateutil import tz
from django.contrib.auth.models import User

from django.db.models import *
from django.utils.timezone import now


def rand_range(range):
    return range[0] + random.random() * range[1]


class MeterInfo(Model):
    user = OneToOneField('auth.User', related_name='meter_info', on_delete=CASCADE)

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
