from allauth.socialaccount.models import SocialApp
from django.contrib.auth import logout as logout_fn
from django.shortcuts import redirect


from project.settings import OAUTH_SERVER_BASEURL


def logout(request):
    # clear session
    logout_fn(request)

    # get client id
    client_id = ""
    app = SocialApp.objects.filter(provider="keyrockprovider").first()
    if app:
        client_id = f"&client_id={app.client_id}"
        print(client_id)

    # logout from keyrock
    return redirect(f"{OAUTH_SERVER_BASEURL}/auth/external_logout?_method=DELETE&{client_id}")
