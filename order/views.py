from django.contrib import messages
from django.shortcuts import redirect, render

from cart.models import *
from userdash.models import *

# Create your views here.

def orderverification(request):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    address = UserAddress.objects.filter(user=current_user,is_deleted=False)  
    new_total = sum(item.sub_total() for item in cart_items) 

    payment_option = request.POST.get('payment_option')
    print(payment_option)
    
    if payment_option is None:
            messages.error(request, 'Select Payment Option')
            return redirect('cart:cart_checkout')
        
    if not address:
            messages.error(request, 'Select Address To Continue')
    for cart_item in cart_items:
         
        if not cart_item.variant.variant_status:
             messages.error(request,'variant is unavailable')
             return redirect('cart:list_cart')


        if cart_item.variant.variant_stock < 1:
            messages.error(request, 'Out of stock')
            return redirect('cart:list_cart')
        
        if not cart_item.product.is_active:
                messages.error(request, 'Product unavailable')
                return redirect('cart:list_cart') 
        else:
            messages.success(request, 'Order Success')
            
    return redirect('order:order_success')  



        
        
def order_success(request):


    return render(request, 'Order/order.html')

