"""
            CREATE OR REPLACE VIEW consumptions AS (
                SELECT first_name meter_number,
                    activity,
                    "Lat", "Long",
                    "date",
                    to_char("naiades_dashboard_consumption"."date", 'Day') AS "day",
                    to_char("naiades_dashboard_consumption"."date", 'Month') AS "month",
                    consumption
                FROM naiades_dashboard_consumption
                INNER JOIN naiades_dashboard_meterinfo ON naiades_dashboard_meterinfo.meter_number = naiades_dashboard_consumption.meter_number_id
                INNER JOIN naiades_dashboard_meterinfoaccess ON naiades_dashboard_meterinfoaccess.meter_info_id = naiades_dashboard_meterinfo.meter_number
                INNER JOIN auth_user ON auth_user.id = naiades_dashboard_meterinfoaccess.user_id AND (NOT auth_user.is_staff)
            )
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naiades_dashboard', '0005_remove_meterinfo_user'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW IF EXISTS consumptions;
            CREATE OR REPLACE VIEW consumptions AS (
                SELECT first_name meter_number, 
                    activity, 
                    "Lat", "Long", 
                    "date", 
                    to_char("naiades_dashboard_consumption"."date", 'Day') AS "day", 
                    to_char("naiades_dashboard_consumption"."date", 'Month') AS "month",
                    consumption
                FROM naiades_dashboard_consumption
                INNER JOIN naiades_dashboard_meterinfo ON naiades_dashboard_meterinfo.meter_number = naiades_dashboard_consumption.meter_number_id
                INNER JOIN naiades_dashboard_meterinfoaccess ON naiades_dashboard_meterinfoaccess.meter_info_id = naiades_dashboard_meterinfo.meter_number
                INNER JOIN auth_user ON auth_user.id = naiades_dashboard_meterinfoaccess.user_id AND (NOT auth_user.is_staff)
            )
            """,
            reverse_sql="""
                DROP VIEW IF EXISTS consumptions
            """
        )
    ]