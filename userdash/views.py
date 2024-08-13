
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.

@login_required(login_url='/login/')
def user_profile(request):
    user_address = UserAddress.objects.filter(user=request.user,is_deleted=False).order_by('-status')
    return render(request, 'user_dash/demo.html',{ 'user_address': user_address })


def add_address(request):
    user_addresses = UserAddress.objects.filter(user=request.user).order_by('-status', 'id')
    context = {
        'user_addresses': user_addresses,
    }

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        name = request.POST.get('name')
        house_name = request.POST.get('house_name')
        street_name = request.POST.get('street_name')
        pin_number = request.POST.get('pin_number')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country', 'null')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status') == 'on'
        
        address = UserAddress(
            user=user,
            name=name,
            house_name=house_name,
            street_name=street_name,
            pin_number=pin_number,
            district=district,
            state=state,
            country=country,
            phone_number=phone_number,
            status=status
        )
        if status:
            UserAddress.objects.filter(user=request.user, status=True).update(status=False)
        
        address.save()

        

        messages.success(request, 'Address added successfully.')
        return redirect('userdash:add-address')

    return render(request, 'user_dash/demo.html', context)

def changepass(request):
    if request.method =='POST':
        user = User.objects.get(id=request.user.id)
        old_password = request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        if user.check_password(old_password):
             
            if new_password == confirm_password and new_password != old_password:
                user.set_password(new_password) 
                user.save()
                messages.success(request, 'Password Changed Successfully')


    return render(request, 'user_dash/demo.html')


def edituser(request):
    if request.method=="POST":
        user = User.objects.get(id=request.user.id)
        print(user)
        user.first_name=request.POST.get('firstname')
        user.last_name=request.POST.get('lastname')
        user.email=request.POST.get('email')
        user.save()

    return render(request,'user_dash/demo.html')


def default(request,pk):
        address= UserAddress.objects.get(id=pk,user=request.user)
        default = UserAddress.objects.filter(user=request.user, status=True).update(status=False)
        address.status = True
        address.save()

        return redirect('userdash:user-profile')  


def delete(request,pk):
    address= UserAddress.objects.get(id=pk,user=request.user)
    address.is_deleted=True
    address.save()
    return redirect('userdash:user-profile')
   
        