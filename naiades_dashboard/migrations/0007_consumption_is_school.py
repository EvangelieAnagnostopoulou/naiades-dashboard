# Generated by Django 2.0 on 2020-03-28 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naiades_dashboard', '0006_consumptionsview'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumption',
            name='is_school',
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
            """
            UPDATE "naiades_dashboard_consumption"
            SET is_school = ("naiades_dashboard_meterinfo"."activity" = 'School')
            FROM "naiades_dashboard_meterinfo"
            WHERE "naiades_dashboard_consumption"."meter_number_id" = "naiades_dashboard_meterinfo"."meter_number"
            """, reverse_sql=""
        )
    ]
