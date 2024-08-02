from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @login_required(login_url='admindash:admin_login')
    def wrapper(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not authorized to access this page.')
            return redirect('admindash:admin_login')  
    return wrapper