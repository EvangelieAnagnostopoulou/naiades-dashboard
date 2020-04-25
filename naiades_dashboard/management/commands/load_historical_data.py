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
        existing_meter_ids = {
            meter_info.meter_nubmer: meter_info for meter_info in MeterInfo.objects.all()
        }

        # drop all
        Consumption.objects.all().delete()

        with open(data_path, 'r', encoding='utf-8') as inp_f:
            reader = csv.DictReader(inp_f)

            consumptions = []
            for row in tqdm.tqdm(reader):
                meter_id = row['Meter ID']

                # get meter info
                meter_info = existing_meter_ids.get(meter_id)

                # check if exists in db
                if not meter_info:
                    continue

                # parse timestamp
                t = datetime.strptime(row['Timestamp'], '%d/%m/%Y %H:%M').\
                    replace(tzinfo=pytz.UTC)

                # add record
                consumptions.append(Consumption.parse_and_create(
                    meter_number_id=meter_id,
                    activity=meter_info.activity,
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

