from django.http import HttpResponseForbidden
from rest_framework.authtoken.models import Token

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            try:
                _, token = request.headers['Authorization'].split()
                user = Token.objects.get(key=token).user
                request.user = user
                if not request.user:
                    return HttpResponseForbidden("Not Authenticated")
            except Token.DoesNotExist:
                return HttpResponseForbidden("Invalid Token.")
            except ValueError:
                return HttpResponseForbidden("Please enter your token.")
        response = self.get_response(request)
        return response
