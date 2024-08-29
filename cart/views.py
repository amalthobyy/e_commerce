from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from userdash.models import *
from coupon.models import *

from .models import *       
from product.models import * 
from django.contrib import messages



def add_to_cart(request):
    print("Add to cart view called")
    if request.method == "POST":
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity',1))


        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        variant = get_object_or_404(Product_Variant, id=variant_id)
        product = get_object_or_404(Products, id=variant.product.id)

        if quantity > 5:
            messages.error(request, "Quantity Limit Exceed")
            return redirect('product:product-detailsuser', pk=product.id)
        
        # if quantity > variant.variant_stock:
        #     messages.error(request, "Not Enough Quantity Left")
        #     return redirect('product:product-detailsuser', pk=product.id)
        
        if variant.variant_stock < 1:
            messages.error(request, "Product out of stock")
            return redirect('product:product-detailsuser', pk=product.id)
        
        if not product.is_active:
            messages.error(request, "Product is unavailable")
            return redirect('product:product-detailsuser', pk=product.id)

        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': 1}
        )

        if not created:
            # Check if adding the quantity exceeds the limit of 5
            if cart_item.quantity + quantity > 5:
                messages.error(request, "Quantity Limit Exceed for this item")
                return redirect('product:product-detailsuser', pk=product.id)
            
            # Update the quantity
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, 'Product added to cart successfully')
        return redirect('product:product-detailsuser', pk=product.id)
    



def list_cart(request):
     
     cart = get_object_or_404(Cart, user=request.user)
     cart_item = CartItem.objects.filter(cart=cart).order_by('-cart__updated_at')
     cart_prices = CartItem.objects.filter(cart=cart, is_active=True)
    
     cart_total = sum(item.sub_total() for item in cart_prices)


     
     return render(request,'cart/cart.html',{'cart':cart, 'cart_item':cart_item, 'cart_total':cart_total})


def update_is_active(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        is_active = request.POST.get('is_active') == 'true'

        try:
            item = CartItem.objects.get(id=item_id)
            item.is_active = is_active
            item.save()  # Ensure this saves the change to the database
            
            # Recalculate the cart total for active items
            cart = get_object_or_404(Cart, user=request.user)
            cart_prices = CartItem.objects.filter(cart=cart, is_active=True)
            
            cart_total = int(sum(item.sub_total() for item in cart_prices))
            cart_subtotal = cart_total
            cart_item_total = int(item.sub_total())
            

            return JsonResponse({'success': True, 'cart_total': cart_total,'cart_subtotal':cart_subtotal,'cart_item_total':cart_item_total})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    


def update_cart_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('quantity'))

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.quantity = new_quantity
        cart_item.save()

        # Recalculate the new total and subtotal
        cart_items = CartItem.objects.filter(cart__user=request.user, is_active=True)
        new_total = sum(item.sub_total() for item in cart_items)
        cart_item_total = cart_item.sub_total()

        response = {
            'success': True,
            'new_total': round(new_total, 2),
            'item_sub_total': round(new_total, 2),  # Subtotal for the specific item
            'cart_item_total': round(cart_item_total, 2) 
        }

        return JsonResponse(response)

    return JsonResponse({'success': False}, status=400)


def cart_checkout(request):
     
    cart = Cart.objects.get(user= request.user)
    cart_items = CartItem.objects.filter(cart=cart,is_active=True)
    


    if not cart_items.exists():
        messages.error(request, 'Select Product')
        return redirect('cart:list_cart')
     

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
        
    cart_total = sum(item.sub_total() for item in cart_items)


    available_coupons = Coupon.objects.filter(status=True, expiry_date__gte=timezone.now()) 
    used_coupons = UserCoupon.objects.filter(user=request.user).values_list('coupon',flat=True) 
    available_coupons = available_coupons.exclude(id__in=used_coupons)

    coupon_code = request.session.get('applied_coupon', None)
    discount = 0
    coupon_name = "Not Applied"
    if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                discount = coupon.maximum_amount
                coupon_name = coupon.coupon_name
                discount_amount = (cart_total * discount / 100)
                if discount_amount > discount:
                    discount_amount = discount
                cart_total -= discount_amount
            except Coupon.DoesNotExist:
                pass
            

    user_address = UserAddress.objects.filter(user=request.user.id,is_deleted=False).order_by('-status', 'id')

    return render(request,'cart/checkout.html', {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'user_address': user_address,
            'discount':discount,
            'coupon_name':coupon_name,
            'available_coupons': available_coupons,
            })

def remove_item_cart(request,pk):
     
    cart_items = CartItem.objects.get(id=pk)
    cart_items.delete()


    return redirect('cart:list_cart')

        
        
@csrf_exempt
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        response = {'success': False}
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            current_total = sum(item.sub_total() for item in cart_items)
        except Cart.DoesNotExist:
            response['message'] = 'Cart not found.'
            return JsonResponse(response)

        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                
                if current_total >= coupon.minimum_amount:
                    discount = coupon.discount
                    discount_amount = (current_total * discount / 100)

                    # Cap the discount amount to the maximum amount
                    discount_amount = min(discount_amount, coupon.maximum_amount)
                    
                    new_total = current_total - discount_amount

                    response.update({
                        'success': True,
                        'message': 'Coupon applied successfully.',
                        'current_total': current_total,
                        'new_total': new_total,
                        'discount': discount,
                        'discount_amount': discount_amount
                    })
                    
                    request.session['applied_coupon'] = coupon_code
                else:
                    response['message'] = f'Coupon only available for orders over {coupon.minimum_amount}'
            except Coupon.DoesNotExist:
                response['message'] = 'Invalid coupon code.'
        else:
            new_total = sum(item.sub_total() for item in cart_items)
            response.update({
                'success': True,
                'new_total': new_total,
                'discount': 0,
                'discount_amount': 0,
            })

        return JsonResponse(response)

@csrf_exempt
def remove_coupon(request):
    if request.method == 'POST':
        response = {'success': False}
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        request.session.pop('applied_coupon', None)

        new_total = sum(item.sub_total() for item in cart_items)
        response.update({
            'success': True,
            'message': 'Coupon removed successfully.',
            'new_total': new_total,
            'discount': 0
        })

        return JsonResponse(response)  





    