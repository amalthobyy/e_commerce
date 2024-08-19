
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from order.models import *

from .models import *
# Create your views here.

@login_required(login_url='/login/')
def user_profile(request):
    orders= OrderMain.objects.filter(user=request.user.id)
    user_address = UserAddress.objects.filter(user=request.user,is_deleted=False).order_by('-status')
    return render(request, 'user_dash/demo.html',{ 'user_address': user_address ,'orders':orders})


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
        status = request.POST.get('status') == "on"
        
        address = UserAddress.objects.create(
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
            if new_password != confirm_password:
                messages.error(request,"new password is  not matching")    


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

def edit_address(request, pk):
    address = get_object_or_404(UserAddress, id=pk, user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        house_name = request.POST.get('house_name').strip()
        street_name = request.POST.get('street_name').strip()
        pin_number = request.POST.get('pin_number').strip()
        district = request.POST.get('district').strip()
        state = request.POST.get('state').strip()
        country = request.POST.get('country', 'null').strip()
        phone_number = request.POST.get('phone_number').strip()
        status = request.POST.get('status') == "on"

        # Validate required fields
        if not name or not house_name or not street_name or not pin_number or not district or not state or not country or not phone_number:
            messages.error(request, "All fields are required.")
            return redirect('userdash:edit_address', pk=pk)

        # Validate pin number
        if not pin_number.isdigit() or len(pin_number) != 6:
            messages.error(request, "Please enter a valid 6-digit PIN number.")
            return redirect('userdash:edit_address', pk=pk)

        # Validate phone number
        if not phone_number.isdigit() or len(phone_number) not in [10, 12]:
            messages.error(request, "Please enter a valid phone number with 10 or 12 digits.")
            return redirect('userdash:edit_address', pk=pk)

        # Update the address
        address.name = name
        address.house_name = house_name
        address.street_name = street_name
        address.pin_number = pin_number
        address.district = district
        address.state = state
        address.country = country
        address.phone_number = phone_number

        # Handle the status update
        if status:
            UserAddress.objects.filter(user=request.user, status=True).update(status=False)
        address.status = status

        address.save()

        messages.success(request, 'Address updated successfully.')
        return redirect('userdash:user-profile')

    context = {
        'address': address,
    }
    return render(request, 'userdash/demo.html', context)



def toggle_address_status(request):
    if request.method == 'POST':
        try:
            address_id = request.POST.get('address_id')
            
            address = get_object_or_404(UserAddress, id=address_id, user=request.user, is_deleted=False)

            # Set all addresses to inactive
            UserAddress.objects.filter(user=request.user).update(order_status=False)
            
            # Set the selected address to active
            address.order_status = True
            address.save()
            
            return JsonResponse({'success': True})
        except UserAddress.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Address not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


 
def add_addresstwo(request):
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
        return redirect('cart:cart_checkout')

    return render(request, 'user_dash/addaddress.html', context)      