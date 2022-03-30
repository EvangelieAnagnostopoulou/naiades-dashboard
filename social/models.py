import pytz

from django.db.models import *


cet_timezone = pytz.timezone("Europe/Madrid")


class Tweet(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    user = ForeignKey('auth.User', on_delete=CASCADE, related_name='tweets')
    is_deleted = BooleanField(default=False)
    is_accepted = BooleanField(default=False)
    message = TextField()

    def to_dict(self):
        # convert timestamps to CET since this is our primary audience
        # TODO allow users to select preferred timezone
        return {
            'id': self.id,
            'user': {
                'id': self.user_id,
                'meter_number': self.user.username,
                'name': self.user.first_name,
            },
            'created': self.created.astimezone(cet_timezone).strftime('%d/%m/%Y %H:%M'),
            'updated': self.updated.astimezone(cet_timezone).strftime('%d/%m/%Y %H:%M'),
            'message': self.message,
            'is_deleted': self.is_deleted,
            'is_accepted': self.is_accepted,
        }
