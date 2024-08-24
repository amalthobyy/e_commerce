from django.db import IntegrityError
from .models import *
from social_core.pipeline.partial import partial
from django.contrib import messages

@partial
def save_user_details(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    email = details.get('email')
    first_name = details.get('first_name', '')
    last_name = details.get('last_name', '')

    if not email or not first_name:
        return strategy.redirect('accounts:login')  # Handle the error

    try:
        # Attempt to create the user
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        is_new = True
    except IntegrityError:
        # Handle the case where the email already exists
        user = User.objects.get(email=email)
        is_new = False

    return {
        'is_new': is_new,
        'user': user
    }


def activate_user(user, *args, **kwargs):
    user.is_active = True
    user.save()

def check_if_user_blocked(strategy, user, *args, **kwargs):
    if user.is_blocked:
        # Add an error message
        messages.error(strategy.request, "Your account is blocked. Please contact support.")
        return strategy.redirect('accounts:home')  # Redirect to an error page for blocked users

    return {
        'is_blocked': False,
        'user': user
    }