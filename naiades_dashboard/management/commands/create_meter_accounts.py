import os
import csv
import tqdm

from django.core.management.base import BaseCommand

from naiades_dashboard.models import *
from project.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Create meter accounts'

    # def add_arguments(self, parser):
    #     parser.add_argument('path', type=str, help='Path to meter info CSV')

    ACTIVITIES = [
        'School',
        'Irrigation Hydrant',
        'Municipal Office',
        'House',
        'Municipal Sport Facility',
        'Fire Hydrant',
        'Fire Fire Hydrant',
        'Font',
        'Other Sport Facility',
        'Public Garden',
    ]

    TEMP_PASSWORD = 'pass1234'

    def handle(self, *args, **kwargs):
        meter_info_path = os.path.join(BASE_DIR, 'naiades_dashboard/data/meter_info.csv')

        # confirm action
        if input('This will drop all database data - are you sure you want to continue? (y/n): ').lower() != 'y':
            return

        # drop all
        MeterInfo.objects.all().delete()

        # count based on activity
        activity_cnt = {activity: 0 for activity in self.ACTIVITIES}

        # parse data
        with open(meter_info_path, 'r', encoding='utf-8') as inp_f:
            reader = csv.DictReader(inp_f)

            meter_infos = []
            # for each meter info row
            for row in tqdm.tqdm(reader):

                # get activity & count
                activity = row['Activity']
                activity_norm = activity.replace(' ', '')
                activity_cnt[activity] += 1
                cnt = activity_cnt[activity]

                # create user
                user = User.objects.create(
                    username='%s%02d' % (activity_norm, cnt),
                    first_name=f'{activity} {cnt}'
                )

                # set temp password
                user.set_password(self.TEMP_PASSWORD)
                user.save()

                # add meter info
                meter_infos.append(MeterInfo(
                    meter_number=row['Meter ID'],
                    activity=activity,
                    latitude=row['Latitude'],
                    longitude=row['Longitude'],
                    user=user
                ))

        # save to db
        MeterInfo.objects.bulk_create(meter_infos)
