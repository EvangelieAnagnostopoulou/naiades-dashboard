from django.db.models import *


class Consumption(Model):
    consumption_id = IntegerField(primary_key=True, db_column="consumption_id")
    household_id = CharField(max_length=256, db_column='Id')
    consumption = DecimalField(max_digits=16, decimal_places=10, db_column="Consumption")

    day = CharField(max_length=64, db_column="Day")
    hour = SmallIntegerField(db_column="Hour")
    hour_idx = SmallIntegerField(db_column="Counter")

    latitude = DecimalField(max_digits=24, decimal_places=4, db_column="Lat")
    longitude = DecimalField(max_digits=24, decimal_places=4, db_column="Lon")

    class Meta:
        db_table = 'water_weekly'
        managed = True
