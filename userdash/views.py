
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from order.models import *
from product.models import *

from .models import *

# Create your views here.

@login_required(login_url='/login/')
def user_profile(request):
    orders= OrderMain.objects.filter(user=request.user.id).order_by('-updated_at')
    user_address = UserAddress.objects.filter(user=request.user,is_deleted=False).order_by('-status')
    return render(request, 'user_dash/demo.html',{ 'user_address': user_address ,'orders':orders})


def add_address(request):
    user_addresses = UserAddress.objects.filter(user=request.user).order_by('-status', 'id')
    context = {
        'user_addresses': user_addresses,
    }

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        name = request.POST.get('name').strip()
        house_name = request.POST.get('house_name').strip()
        street_name = request.POST.get('street_name').strip()
        pin_number = request.POST.get('pin_number').strip()
        district = request.POST.get('district').strip()
        state = request.POST.get('state').strip()
        country = request.POST.get('country', 'null').strip()
        phone_number = request.POST.get('phone_number').strip()
        status = request.POST.get('status') == "on"

        if not name:
            messages.error(request, 'Name Required')
        
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

    if request.method == 'POST':
        print("posu")
        user=request.user.id
        address = get_object_or_404(UserAddress, id=pk, user=user)
        name = request.POST.get('name')
        house_name = request.POST.get('house_name')
        street_name = request.POST.get('street_name')
        pin_number = request.POST.get('pin_number')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country', '')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status') == "on"

        # Validate required fields
        if not name or not house_name or not street_name or not pin_number or not district or not state or not country or not phone_number:
            print("ff")
            messages.error(request, "All fields are required.")
            return redirect('userdash:user-profile')

        # Validate pin number
        if not pin_number.isdigit() or len(pin_number) != 6:
            print("pn")
            messages.error(request, "Please enter a valid 6-digit PIN number.")
            return redirect('userdash:user-profile')

        # Validate phone number
        if not phone_number.isdigit() or len(phone_number) not in [10, 12]:
            print("ph")
            messages.error(request, "Please enter a valid phone number with 10 or 12 digits.")
            return redirect('userdash:user-profile')

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
            UserAddress.objects.filter(user=user, status=True).update(status=False)
        address.status = status

        address.save()

        messages.success(request, 'Address updated successfully.')
        return redirect('userdash:user-profile',)
    else:
        messages.error(request, 'Address Not Found')
        return redirect('userdash:user-profile',)




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
        name = request.POST.get('name').strip()
        house_name = request.POST.get('house_name').strip()
        street_name = request.POST.get('street_name').strip()
        pin_number = request.POST.get('pin_number').strip()
        district = request.POST.get('district').strip()
        state = request.POST.get('state').strip()
        country = request.POST.get('country', 'null').strip()
        phone_number = request.POST.get('phone_number').strip()
        status = request.POST.get('status') == 'on'
        
        if not name:
            messages.error(request, 'Name Required')
            return redirect('cart:cart_checkout')

        if not house_name:
            messages.error(request, 'house name Required')
            return redirect('cart:cart_checkout')

        if not street_name:
            messages.error(request, 'street name Required')
            return redirect('cart:cart_checkout')

        if not pin_number:
            messages.error(request, 'pin number Required')
            return redirect('cart:cart_checkout')

        if not district:
            messages.error(request, 'district Required')
            return redirect('cart:cart_checkout')

        if not state:
            messages.error(request, 'state Required')
            return redirect('cart:cart_checkout')

        if not country:
            messages.error(request, 'Name Required')
            return redirect('cart:cart_checkout')

        if not phone_number:
            messages.error(request, 'phone number Required')
            return redirect('cart:cart_checkout')

        if not pin_number.isdigit() or len(pin_number) != 6:
            messages.error(request, "Please enter a valid 6-digit PIN number.")
            return redirect('cart:cart_checkout')
        
        if not phone_number.isdigit() or len(phone_number) not in [10, 12]:
            messages.error(request, "Please enter a valid phone number with 10 or 12 digits.")
            return redirect('cart:cart_checkout')
        

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


from django.http import JsonResponse



def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Products.objects.filter(
            product_name__icontains=query
        ) | Products.objects.filter(
            product_brand__brand_name__icontains=query
        ) | Products.objects.filter(
            product_description__icontains=query
        )
        
        data = {
            'results': [
                {
                    'name': result.product_name,
                    'url': f'/product/product-details/{result.id}/',  # Ensure this matches your URL pattern
                    'thumbnail': result.thumbnail.url if result.thumbnail else ''
                }
                for result in results
            ]
        }
    else:
        data = {'results': []}

    return JsonResponse(data)



def add_to_wishlist(request):
    if request.method == "POST":
        variant_id = request.POST.get('variant_id')

        if not variant_id:
            return JsonResponse({'status': 'error', 'message': 'Variant ID is missing'})

        try:
            variant = Product_Variant.objects.get(id=variant_id)
        except Product_Variant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Variant does not exist'})

        user = request.user
        wishlist, created = Wishlist.objects.get_or_create(user=user,variant=variant)

        messages.success(request, 'Added To Wishlist') 
        return JsonResponse({'status': 'added'})
    
    print("Invalid request method")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def wishlist(request):
    user= User.objects.get(id=request.user.id)
    wishlists =Wishlist.objects.filter(user=user)

    return render(request,'user_dash/wishlist.html',{'wishlists':wishlists})
   
def remove_wishlist(request,pk):

    try:
        item = get_object_or_404(Wishlist, id=pk)
        item.delete()
        return redirect('userdash:wishlist')
    except:
        return redirect('userdash:wishlist')





