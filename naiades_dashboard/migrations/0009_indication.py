# Generated by Django 2.0 on 2021-11-07 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('naiades_dashboard', '0008_auto_20201230_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('consumption', models.DecimalField(decimal_places=16, max_digits=32)),
                ('meter_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indications', to='naiades_dashboard.MeterInfo')),
            ],
        ),
    ]
