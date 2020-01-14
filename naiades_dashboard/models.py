import random
from datetime import datetime, timedelta

import tqdm
from dateutil import tz

from django.db.models import *
from django.utils.timezone import now


def rand_range(range):
    return range[0] + random.random() * range[1]


class Consumption(Model):
    meter_number = CharField(max_length=250, db_column="MeterNumber")
    gis_agua_id = CharField(max_length=250, db_column="GISAguaID")
    activity = CharField(max_length=250, db_column="Activity")
    periodicity = CharField(max_length=250, db_column="Periodicity")

    consumption = DecimalField(max_digits=32, decimal_places=16, db_column="Consumption")

    date = DateTimeField(db_column="date")
    year = SmallIntegerField(db_column="Year")
    month = SmallIntegerField(db_column="Month")
    week = SmallIntegerField(db_column="Week")
    day = SmallIntegerField(db_column="Day")
    hour = SmallIntegerField(db_column="Hour")

    latitude = DecimalField(max_digits=16, decimal_places=8, db_column="Lat")
    longitude = DecimalField(max_digits=16, decimal_places=8, db_column="Long")

    class Meta:
        db_table = 'data'
        managed = True

    @staticmethod
    def generate_random_data(n_meters=1000):
        from_date = datetime(2020, 1, 1).replace(tzinfo=tz.tzutc())
        to_date = now()

        lats = (38.34, 0.01)
        longs = (-0.49, 0.01)
        consumptions_range = (10, 90)
        activities = [
            'Public Gardens',
            'Hydrants',
            'Other Sport facilities',
            'Houses',
            'Fonts',
            'Schools',
            'Municipal Sport facilities',
            'Fire Hydrants',
            'Municipal offices',
            'Irrigation hydrant',
        ]

        # clear all data
        Consumption.objects.all().delete()

        for meter_idx in tqdm.tqdm(range(n_meters)):
            # for each meter
            # choose a random activity
            activity = random.choice(activities)

            meter_max_consumption = rand_range(consumptions_range)

            # set random location
            lat, long = rand_range(lats), rand_range(longs)

            # add data
            dt = from_date
            consumptions = []
            while dt <= to_date:
                # get week
                week_idx = dt.isocalendar()[1]

                # random consumption based on week
                # on average falls as weeks go by
                consumption = random.random() * meter_max_consumption * max(20 - week_idx / 20, 0.5)

                # add record
                consumptions.append(Consumption(
                    meter_number='%06d' % meter_idx,
                    activity=activity,
                    periodicity="HOURLY",
                    date=dt,
                    year=dt.year,
                    month=dt.month,
                    week=week_idx,
                    day=dt.weekday(),
                    hour=dt.hour,
                    latitude=lat,
                    longitude=long,
                    consumption=consumption
                ))

                # move to next
                dt += timedelta(hours=1)

            # insert all
            Consumption.objects.bulk_create(consumptions)
