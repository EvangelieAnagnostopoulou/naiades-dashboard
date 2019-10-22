from django.shortcuts import redirect


class AuthRequiredMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.path == '/webhook/Q0wzM1pAZAXai084pF34zrTRsv2MAZz3/':
            return self.get_response(request)

        if request.path == '/login/':
            return self.get_response(request)

        if request.path.startswith('/admin'):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('/login/')

        response = self.get_response(request)

        if request.path.startswith('/logout'):
            return redirect('/login/')

        return response
