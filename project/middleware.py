import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from project.settings import LOGIN_URL, LOGOUT_URL, STATIC_URL


class AuthRequiredMiddleware(object):

    whitelisted_prefixes = [
        LOGIN_URL,
        STATIC_URL,
        "/admin",
        "/keyrock/",
        "/keyrockprovider/login/",
        '/webhook/Q0wzM1pAZAXai084pF34zrTRsv2MAZz3/'
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if any(
            [request.path.startswith(prefix) for prefix in self.whitelisted_prefixes]
        ):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect(LOGIN_URL)

        response = self.get_response(request)

        if request.path.startswith(LOGOUT_URL):
            return redirect(LOGIN_URL)

        if not request.user.is_authenticated:
            return redirect(f'{LOGIN_URL}/?next={request.get_full_path()}')

        return response


class NonHtmlDebugToolbarMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        debug = request.GET.get('debug', 'UNSET')

        if debug != 'UNSET':
            if response['Content-Type'] == 'application/octet-stream':
                new_content = '<html><body>Binary Data, ' \
                    'Length: {}</body></html>'.format(len(response.content))
                response = HttpResponse(new_content)
            elif response['Content-Type'] != 'text/html':
                content = response.content
                try:
                    json_ = json.loads(content)
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse('<html><body><pre>{}'
                                        '</pre></body></html>'.format(content))

        return response
