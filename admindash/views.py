from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import User 
from order.models import *
from utils.decorators import admin_required


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_admin:
                login(request, user)
                return redirect('admindash:admin_home')
            else:
                messages.error(request, 'You are not authorized to access this page.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'admindash/admin_login.html')


@admin_required
def admin_home(request):
    return render(request,'admindash/admin_dash.html')

@admin_required
def list_user(request):
    users = User.objects.filter(is_admin=False)
    return render(request, 'admindash/list_user.html', {'users': users})
@admin_required
def user_block(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = True
    user.save()
    messages.success(request, 'User blocked successfully.')
    return redirect('admindash:list_user')


@admin_required
def user_unblock(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = False
    user.save()
    messages.success(request, 'User unblocked successfully.')
    return redirect('admindash:list_user')

def order_status(request,pk):
    if request.method == 'POST':
        fk = pk
        order = get_object_or_404(OrderMain, id=pk)
        new_status = request.POST.get('order_status')
        
    if new_status:
        order.order_status = new_status
        order.save()
            
        return redirect('order:admin_orders_details',fk)
    else:
        return HttpResponse("No status selected", status=400)