from django.db import migrations

from naiades_dashboard.managers.users import MeterUserManager


def recreate_users(apps, schema_editor):
    # get models at this stage
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    MeterInfo = apps.get_model("naiades_dashboard", "MeterInfo")
    MeterInfoAccess = apps.get_model("naiades_dashboard", "MeterInfoAccess")

    # drop users except for superusers
    User.objects.filter(is_superuser=False).delete()

    # start a user manager
    manager = MeterUserManager(
        models={
            "User": User,
            "Group": Group,
            "MeterInfoAccess": MeterInfoAccess,
        }
    )

    # recreate for all existing school meters
    for idx, meter_info in enumerate(MeterInfo.objects.filter(activity="School")):
        manager.create_users(meter_info=meter_info, forced_count=idx)


class Migration(migrations.Migration):

    dependencies = [
        ('naiades_dashboard', '0009_auto_20211205_1638'),
    ]

    operations = [
        migrations.RunPython(recreate_users, reverse_code=lambda _, __: None),
    ]
