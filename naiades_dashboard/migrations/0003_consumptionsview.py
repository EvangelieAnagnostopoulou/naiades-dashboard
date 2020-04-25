# Generated by Django 2.0 on 2020-03-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naiades_dashboard', '0002_auto_20200315_2054'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW consumptions AS (
                SELECT first_name meter_number, activity, "Lat", "Long", "date", consumption
                FROM naiades_dashboard_consumption
                INNER JOIN naiades_dashboard_meterinfo ON naiades_dashboard_meterinfo.meter_number = naiades_dashboard_consumption.meter_number_id
                INNER JOIN auth_user ON auth_user.id = naiades_dashboard_meterinfo.user_id
            )
            """,
            reverse_sql="""
                DROP VIEW IF EXISTS consumptions
            """
        )
    ]
