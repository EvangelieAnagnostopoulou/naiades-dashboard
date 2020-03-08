from django.db.models import *


class Tweet(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    user = ForeignKey('auth.User', on_delete=CASCADE, related_name='tweets')
    is_deleted = BooleanField(default=False)
    message = TextField()

    def to_dict(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user_id,
                'meter_number': self.user.username,
                'name': self.user.first_name,
            },
            'created': self.created.strftime('%d/%m/%Y %H:%I'),
            'updated': self.updated.strftime('%d/%m/%Y %H:%I'),
            'message': self.message,
            'is_deleted': str(self.is_deleted),
        }
