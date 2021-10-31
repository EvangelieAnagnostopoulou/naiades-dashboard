from allauth.account.utils import perform_login
from django.contrib.auth.models import User

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class KeyRockAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        # ignore if user exists
        if sociallogin.user.id:
            return

        # try to connect based on username
        try:
            user = User.objects.get(username=sociallogin.user.username)
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except User.DoesNotExist:
            pass

        # mark test-user as admin
        if sociallogin.user.email == 'test-user@example.com':
            sociallogin.user.is_staff = sociallogin.user.is_superuser = True
