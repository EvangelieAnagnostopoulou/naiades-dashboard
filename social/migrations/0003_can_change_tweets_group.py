# Generated by Django 2.0 on 2020-03-23 16:48

from django.conf import settings
from django.contrib.auth.models import User
from django.db import migrations, models
import django.db.models.deletion


def create_can_change_tweets_group_set_admins(apps, schema_editor):
    # get models at this stage
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")

    # get tweet content type
    tweet_content_type = ContentType.objects.get(app_label='social', model='tweet')

    # get permissions
    change_tweet_permission = Permission.objects.get(codename='change_tweet')
    delete_tweet_permission = Permission.objects.get(codename='delete_tweet')

    # create tweet admins group & add permissions for this content type
    group = Group.objects.create(name='Tweet Admins')
    group.permissions.add(change_tweet_permission)
    group.permissions.add(delete_tweet_permission)

    # add all admin users to group
    for user in User.objects.filter(is_superuser=False, is_staff=True):
        group.user_set.add(user)


def delete_tweets_group(apps, schema_editor):
    # get models at this stage
    Group = apps.get_model("auth", "Group")

    # delete group
    Group.objects.get(name='Tweet Admins').delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0002_tweet_is_accepted'),
    ]

    operations = [
        migrations.RunPython(create_can_change_tweets_group_set_admins, reverse_code=delete_tweets_group),
    ]