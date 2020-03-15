import os
import csv

import pytz
import tqdm

from django.core.management.base import BaseCommand

from naiades_dashboard.models import *
from project.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Load historical data'

    def handle(self, *args, **kwargs):
        data_path = os.path.join(BASE_DIR, 'naiades_dashboard/data/historical.min.csv')

        # confirm action
        if input('This will drop all database data - are you sure you want to continue? (y/n): ').lower() != 'y':
            return

        # load existing meter ids
        existing_meter_ids = set(MeterInfo.objects.values_list('meter_number', flat=True))

        # drop all
        Consumption.objects.all().delete()

        with open(data_path, 'r', encoding='utf-8') as inp_f:
            reader = csv.DictReader(inp_f)

            consumptions = []
            for row in tqdm.tqdm(reader):
                meter_id = row['Meter ID']

                # check if exists in db
                if meter_id not in existing_meter_ids:
                    continue

                # parse timestamp
                t = datetime.strptime(row['Timestamp'], '%d/%m/%Y %H:%M').\
                    replace(tzinfo=pytz.UTC)

                # add record
                consumptions.append(Consumption.parse_and_create(
                    meter_number_id=meter_id,
                    consumption=row['Consumption'],
                    timestamp=t,
                    estimated=row['Real?'].lower() != 'y'
                ))

                # bulk save
                if len(consumptions) > 1000:
                    Consumption.objects.bulk_create(consumptions)
                    consumptions = []

            # save any remaining
            if consumptions:
                Consumption.objects.bulk_create(consumptions)

