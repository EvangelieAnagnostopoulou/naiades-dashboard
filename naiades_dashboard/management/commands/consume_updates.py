import os
import csv
import pytz
import pysftp

from django.core.management.base import BaseCommand
from django.db import transaction

from naiades_dashboard.models import *
from project.settings import FTP, BASE_DIR


class UpdateFileRecord(object):

    def __init__(self, path, filename, local_filename):
        self.path = path
        self.filename = filename
        self.local_filename = local_filename

    def set_as_parsed(self):
        UpdateFile.objects.create(path=self.path, filename=self.filename)


class Command(BaseCommand):
    help = 'Consume data updates from project FTP'

    # paths to look at for new deliveries
    PATHS = [
        'AMAEM_INC_COLEGIOS',
        'AMAEM_INC_MUNICIPALES',
    ]

    # downloads path
    DOWNLOADS_PATH = os.path.join(BASE_DIR, 'downloads')

    def pull_deliveries(self):
        # TODO revisit this, seems that host key can not be verified now
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(FTP['HOST'], username=FTP['USERNAME'], password=FTP['PASSWORD'], cnopts=cnopts) as sftp:
            for path in self.PATHS:
                with sftp.cd(path):  # temporarily chdir to public

                    # foreach file in the directory
                    for filename in sftp.listdir():

                        # ignore already processed files
                        if UpdateFile.objects.filter(path=path, filename=filename).exists():
                            continue

                        # download
                        local_filename = os.path.join(self.DOWNLOADS_PATH, f'{path.replace("/", "-")}-{filename}')

                        sftp.get(filename, local_filename)

                        # yield record
                        yield UpdateFileRecord(path=path, filename=filename, local_filename=local_filename)

    def parse_record(self, record):
        with transaction.atomic():
            with open(record.local_filename, 'r', encoding='utf-8') as inp_f:

                # open csv reader
                reader = csv.reader(inp_f, delimiter=';')

                # bulk load consumptions
                consumptions = []

                # parse rows
                for row in reader:

                    # parse data
                    meter_number = row[1]
                    consumption = row[3].replace(',', '.')
                    timestamp = datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'). \
                        replace(tzinfo=pytz.UTC)

                    # check if meter exists in database
                    meter_info = MeterInfo.objects.filter(meter_number=meter_number).first()

                    if not meter_info:
                        continue

                    # add consumption record
                    consumptions.append(Consumption.parse_and_create(
                        meter_number_id=meter_number,
                        consumption=consumption,
                        timestamp=timestamp
                    ))

                # bulk save
                Consumption.objects.bulk_create(consumptions)

            # drop local file
            try:
                os.unlink(record.local_filename)
            except:
                pass

            # save record
            UpdateFile.objects.create(path=record.path, filename=record.filename)

    def handle(self, *args, **kwargs):
        # create downloads folder
        if not os.path.exists(self.DOWNLOADS_PATH):
            os.mkdir(self.DOWNLOADS_PATH)

        # pull new deliveries
        with tqdm.tqdm() as bar:
            for record in self.pull_deliveries():

                # update progress
                bar.set_description(f'{record.path} - {record.filename}')
                bar.update(1)

                # parse record
                self.parse_record(record)
