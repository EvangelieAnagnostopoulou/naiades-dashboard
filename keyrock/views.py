import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)

from django.conf import settings

from .provider import KeyRockProvider


class CustomAdapter(OAuth2Adapter):
    provider_id = KeyRockProvider.id
    access_token_url = '{}/oauth2/token/'.format(settings.OAUTH_SERVER_BASEURL)  # Called programmatically, must be reachable from container
    authorize_url = '{}/oauth2/authorize/'.format(settings.OAUTH_SERVER_BASEURL)  # This is the only URL accessed by the browser so must be reachable by the host !
    profile_url = '{}/user/'.format(settings.OAUTH_SERVER_BASEURL)

    def complete_login(self, request, app, token, **kwargs):
        print('complete_login')
        print(request)
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        extra_data['first_name'] = extra_data['username']
        extra_data['last_name'] = ''
        print(extra_data)
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)
