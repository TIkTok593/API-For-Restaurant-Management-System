from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.user.groups.filter(name='DeliveryCrew').exists()  or request.user.groups.filter(name='deliveryCrew').exists():
            return None
        return (request.user, None)