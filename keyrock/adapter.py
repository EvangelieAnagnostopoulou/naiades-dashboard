from django.contrib.auth.models import User

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class KeyRockAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        # try to connect with existing user from local database
        try:
            user = User.objects.get(username=sociallogin.user.username)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass

        # mark test-user as admin
        if sociallogin.user.email == 'test-user@example.com':
            sociallogin.user.is_staff = sociallogin.user.is_superuser = True
