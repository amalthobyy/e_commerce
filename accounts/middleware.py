from typing import Any
from django.shortcuts import redirect, render
from django.contrib import messages
from social_core.exceptions import AuthCanceled  
from django.conf import settings
from django.contrib.auth import logout


class CheckUserBlockedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'is_blocked') and request.user.is_blocked:
                messages.error(request, "Sorry, your account is temporarily suspended. Contact support for help.")
                logout(request)
                return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response


class SocialAuthExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, AuthCanceled):  # Catching specific authentication cancellation exception
            messages.error(request, "Authentication process canceled.")
            return redirect('accounts:home')  # Change 'home' to your desired redirect page
        return None
    


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # If response status code is 404, render the custom 404 page
        if response.status_code == 404:
            return render(request, 'user/404.html', status=404)
        return response