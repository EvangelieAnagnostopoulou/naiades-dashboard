from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import KeyRockProvider

urlpatterns = default_urlpatterns(KeyRockProvider)
