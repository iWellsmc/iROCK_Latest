from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated or isinstance(request.user, AnonymousUser):
            print(f"request.path {request.path}")
            if request.path == reverse('custom_auth:login'):
                return self.get_response(request)
            elif request.path == reverse('custom_auth:adminlogin'):
                return self.get_response(request)
            elif 'from' in request.GET and request.GET['from'] == 'login':
                return self.get_response(request)
            else:
                return redirect(reverse('custom_auth:login'))

        return self.get_response(request)
