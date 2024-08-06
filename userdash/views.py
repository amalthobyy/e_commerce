from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.


def user_profile(request):
    
    return render(request, 'user_dash/demo.html')


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