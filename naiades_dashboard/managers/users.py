import os

from django.contrib.auth.models import User, Group

from naiades_dashboard.models import MeterInfo, MeterInfoAccess


class MeterUserManager(object):

    def __init__(self, models=None, base_count=100, email_domain=None):
        # allow passing models when run in migration
        self.models = models or {
            "User": User,
            "Group": Group,
            "MeterInfoAccess": MeterInfoAccess,
        }

        # user-related config
        self.base_count = base_count
        self.email_domain = email_domain or "example.com"
        self.admin_suffix = "admin"

        # admin group
        self.admin_group, _ = Group.objects.get_or_create(name='Tweet Admins')

    def get_user_info(self, meter_info, forced_count=None):
        # count number of meters with same activity
        # then add one, as well as any base count
        # to calculate next available
        count = self.base_count + \
                (forced_count or MeterInfo.objects.filter(activity=meter_info.activity).count()) + \
                1

        # get username & first name based on activity
        return {
            "username": f"{meter_info.activity.lower().replace(' ', '-')}{count}",
            "first_name": f"{meter_info.activity} {count}",
        }

    def create_users(self, meter_info, forced_count=None):
        # ignore if users already exist
        if MeterInfoAccess.objects.filter(meter_info_id=meter_info.pk).exists():
            return

        # get user info based on count & activity
        info = self.get_user_info(meter_info=meter_info, forced_count=forced_count)

        # create viewer
        viewer = User.objects.create(
            username=f'{info["username"]}',
            email=f'{info["username"]}@{self.email_domain}',
            first_name=f'{info["first_name"]}',
        )

        # create admin user
        admin = User.objects.create(
            username=f'{info["username"]}-{self.admin_suffix}',
            email=f'{info["username"]}-{self.admin_suffix}@{self.email_domain}',
            first_name=f'{info["first_name"]} Admin',
            is_staff=True
        )

        # add admin to group
        self.admin_group.user_set.add(admin)

        # add user accesses
        MeterInfoAccess.objects.bulk_create([
            MeterInfoAccess(user_id=viewer.pk, meter_info_id=meter_info.pk, role='VIEWER'),
            MeterInfoAccess(user_id=admin.pk, meter_info_id=meter_info.pk, role='ADMIN'),
        ])
