from decimal import Decimal
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from cart.models import *
from userdash.models import *
from datetime import datetime, timedelta
from .models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay

# Create your views here.

def orderverification(request):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    address = UserAddress.objects.filter(user=current_user,is_deleted=False,order_status=True).first()
    new_total = sum(item.sub_total() for item in cart_items)
  

    payment_option = request.POST.get('payment_option')
    print(payment_option)
    
    if payment_option is None:
        messages.error(request, 'Select Payment Option')
        return redirect('cart:cart_checkout')
        
    if not address:
        messages.error(request, 'Select Address To Continue')
        return redirect('cart:cart_checkout')

    for cart_item in cart_items:
        if not cart_item.variant.variant_status:
             messages.error(request,'variant is unavailable')
             return redirect('cart:cart_checkout')


        if cart_item.variant.variant_stock < 1:
            messages.error(request, 'Out of stock')
            return redirect('cart:cart_checkout')
        
        if not cart_item.product.is_active:
                messages.error(request, 'Product unavailable')
                return redirect('cart:cart_checkout') 
        

    if payment_option =="Razorpay":
        return redirect('order:razorpay_payment')
    


    if payment_option == "Cash On Delivery":
        
        user = str(request.user.id)
        current_date_time = datetime.now()
        formatted_date_time = current_date_time.strftime("%H%m%S%Y")
        unique = get_random_string(length=4, allowed_chars='1234567890')
        order_id = user + formatted_date_time + unique
        
        formatted_date_time = current_date_time.strftime("%m%Y%H%S")
        unique = get_random_string(length=2, allowed_chars='1234567890')
        payment_id = unique + user + formatted_date_time

        order_address = OrderAddress.objects.create(
             name = address.name,
             house_name = address.house_name,
             street_name = address.street_name,
             pin_number = address.pin_number,
             district = address.district,
             state = address.state,
             country = address.country,
             phone_number = address.phone_number
        )

        order_status = "Confirmed"

        order_main = OrderMain.objects.create(
            user = current_user,
            address = order_address,
            total_amount = new_total,
            order_status = order_status,
            payment_option = payment_option,
            order_id = order_id,
            payment_status = False,
            payment_id = payment_id
        )

        for cart_item in cart_items:
            OrderSub.objects.create(
                user=current_user,
                main_order=order_main,
                variant=cart_item.variant,
                price=cart_item.product.offer_price,
                quantity=cart_item.quantity,
            )

            cart_item.variant.variant_stock -= cart_item.quantity
            cart_item.variant.save()

        cart_items.delete()

        messages.success(request, 'Order Success')        
        return redirect('order:order_success')



     



        
        
def order_success(request):


    return render(request, 'order/order.html')



def list_order_admin(request):
     orders = OrderMain.objects.all().order_by('-updated_at')
     
     return render(request,'order/admin_list_order.html',{'orders':orders})




def admin_orders_details(request,pk):
     orders = OrderMain.objects.get(id=pk)
     order_sub = OrderSub.objects.filter(main_order=orders)

     return render(request, 'order/admin_order_details.html', {'orders': orders, 'order_sub': order_sub}) 



def cancel_order(request, pk):
    try:
        order = OrderMain.objects.get(id=pk)
        order_items = OrderSub.objects.filter(main_order=order, is_active=True)
        reason = request.POST.get('reason','')
        print(reason)
        if not order.is_active:
            messages.error(request, 'Order item is already Canceled.')
            return redirect('userdash:user-profile')
        
        for order_item in order_items:
            order_variant = order_item.variant
            order_quantity = order_item.quantity
            
            order_variant.variant_stock += order_quantity

        order.order_status = "Canceled"
        order.is_active = False
        order.reason =reason
        order.save()
        return redirect('userdash:user-profile')
        
       
            
    
    except OrderMain.DoesNotExist:
        messages.error(request, 'Order does not exist.')
        return redirect('userdash:user-profile')




def razorpay_payment(request):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    address = UserAddress.objects.filter(user=current_user, is_deleted=False, order_status=True).first()
    new_total = sum(item.sub_total() for item in cart_items)

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_order = client.order.create({
        'amount': int(new_total * 100),  # Amount in paise
        'currency': 'INR',
        'payment_capture': '1'
    })
    payment_order_id = payment_order['id']

    user = str(request.user.id)
    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%H%m%S%Y")
    unique = get_random_string(length=4, allowed_chars='1234567890')
    order_id = user + formatted_date_time + unique
    
    formatted_date_time = current_date_time.strftime("%m%Y%H%S")
    unique = get_random_string(length=2, allowed_chars='1234567890')
    payment_id = unique + user + formatted_date_time

    order_address = OrderAddress.objects.create(
        name=address.name,
        house_name=address.house_name,
        street_name=address.street_name,
        pin_number=address.pin_number,
        district=address.district,
        state=address.state,
        country=address.country,
        phone_number=address.phone_number
    )

    # Create an order in your database
    order_main = OrderMain.objects.create(
        user=current_user,
        address=order_address,
        total_amount=new_total,
        order_status="Pending",
        payment_option="Razorpay",
        payment_status=True,
        order_id=order_id,
        payment_id=payment_id
    )

    for cart_item in cart_items:
            OrderSub.objects.create(
                user=current_user,
                main_order=order_main,
                variant=cart_item.variant,
                price=cart_item.product.offer_price,
                quantity=cart_item.quantity,
            )

            cart_item.variant.variant_stock -= cart_item.quantity
            cart_item.variant.save()

    cart_items.delete()

    context = {
        'new_total': int(new_total * 100),
        'api_key': settings.RAZORPAY_KEY_ID,
        'order_id': payment_order_id,
        'order_main_id': order_main.id,  # Pass this to the template
        'user_email': current_user.email,
        'user_phone': current_user.profile.phone if hasattr(current_user, 'profile') else '',
    }

    return render(request, 'cart/razorpay.html', context)

