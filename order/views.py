from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string
from cart.models import *
from userdash.models import *
from datetime import datetime, timedelta
from .models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from coupon.models import*
import razorpay
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from utils.decorators import admin_required
# Create your views here.

def orderverification(request):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    address = UserAddress.objects.filter(user=current_user,is_deleted=False,order_status=True).first()
    cart_total = sum(item.sub_total() for item in cart_items)

    coupon_code = request.session.get('applied_coupon', None)
    discount_amount = 0
    final_amount = cart_total
    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if cart_total >= coupon.minimum_amount:
                discount = coupon.discount
                discount_amount = (cart_total * discount / 100)
                discount_amount = min(discount_amount, coupon.maximum_amount)
                
                final_amount = cart_total - discount_amount
            else:
                messages.error(request, f'Coupon only available for orders over {coupon.minimum_amount}')
        except Coupon.DoesNotExist:
            pass

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
    
    if payment_option =="Wallet":
        user = request.user
        try:
            wallet = Wallet.objects.get(user=user)
            wallet_amount = wallet.balance

            cart_items = CartItem.objects.filter(cart__user=request.user, is_active=True)
            new_total = sum(item.sub_total() for item in cart_items)

            if new_total <= wallet_amount:
                wallet = Wallet.objects.get(user=current_user)
                address = UserAddress.objects.get(user=current_user, order_status=True)
                payment_option = "Wallet Payment"
                
                current_date_time = datetime.now()
                formatted_date_time = current_date_time.strftime("%H%m%S%Y")
                unique = get_random_string(length=4, allowed_chars='1234567890')
                user = str(request.user.id)
                order_id = user + formatted_date_time + unique
                
                formatted_date_time = current_date_time.strftime("%m%Y%H%S")
                unique = get_random_string(length=2, allowed_chars='1234567890')
                payment_id = unique + user + formatted_date_time

                coupon_code = request.session.get('applied_coupon', None)
                discount = 0
                final_amount = new_total
                discount_amount = 0
                
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        discount = coupon.maximum_amount
                        discount_amount = (new_total * discount / 100)
                        if discount_amount > discount:
                            discount_amount = discount
                        final_amount -= discount_amount

                    except Coupon.DoesNotExist:
                        pass
                            
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
                
                order_status = "Confirmed"
                
                order_main = OrderMain.objects.create(
                    user=current_user,
                    address=order_address,
                    total_amount=new_total,
                    final_amount=final_amount,
                    discount_amount=discount_amount,
                    payment_option=payment_option,
                    order_id=order_id,
                    order_status=order_status,
                    payment_id=payment_id,
                    payment_status=True
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
                    
                order_amount = new_total
                description = "Product Purchased With Wallet"
                transaction_type = "Debited"
                
                transaction = Transaction.objects.create(
                    wallet=wallet,
                    description=description,
                    amount=order_amount,
                    transaction_type=transaction_type,
                )

                wallet.balance -= final_amount 
                wallet.save()
                
                cart_items.delete()

                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        used_coupon = UserCoupon.objects.create(
                            user = request.user,
                            coupon = coupon,
                            used = True,
                            order = order_main
                        )

                    except Coupon.DoesNotExist:
                        pass
                
                request.session['order_id'] = order_main.order_id
                request.session['order_date'] = order_main.date.strftime("%Y-%m-%d")
                request.session['order_status'] = order_main.order_status
                
                request.session.pop('applied_coupon', None)
                
                messages.success(request, 'Order Success')
                
                return redirect('order:order_success')
            else:
                messages.error(request, 'Not Enough Money In Wallet')
                return redirect('cart:cart_checkout')
        except Wallet.DoesNotExist:
            messages.error(request, 'Wallet Does Not Exist')
            return redirect('cart:cart_checkout')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('cart:cart_checkout')
    


    if payment_option == "Cash On Delivery":
        cart_items = CartItem.objects.filter(cart__user=request.user, is_active=True)
        new_total = sum(item.sub_total() for item in cart_items)
          
        if cart_total <= 6000: 
            user = str(request.user.id)
            current_date_time = datetime.now()
            formatted_date_time = current_date_time.strftime("%H%m%S%Y")
            unique = get_random_string(length=4, allowed_chars='1234567890')
            order_id = user + formatted_date_time + unique
            
            formatted_date_time = current_date_time.strftime("%m%Y%H%S")
            unique = get_random_string(length=2, allowed_chars='1234567890')
            payment_id = unique + user + formatted_date_time

            coupon_code = request.session.get('applied_coupon', None)
            discount = 0
            final_amount = new_total
            discount_amount = 0
            
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(coupon_code=coupon_code)
                    discount = coupon.maximum_amount
                    discount_amount = (new_total * discount / 100)
                    if discount_amount > discount:
                        discount_amount = discount
                    final_amount -= discount_amount

                except Coupon.DoesNotExist:
                    pass

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
                total_amount = cart_total,
                discount_amount=discount_amount,
                final_amount=final_amount,
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
            
            if coupon_code:
                    try:
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        used_coupon = UserCoupon.objects.create(
                            user = request.user,
                            coupon = coupon,
                            used = True,
                            order = order_main
                        )

                    except Coupon.DoesNotExist:
                        pass

            request.session.pop('applied_coupon', None)

            messages.success(request, 'Order Success')        
            return redirect('order:order_success')
        
        else:
            messages.error(request, 'Cash On Delivery Only Available Upto 6000') 
            return redirect('cart:cart_checkout') 



     



        
        
def order_success(request):
    future_date_time = timezone.now() + timedelta(days=5)
    formatted_future_date = future_date_time.strftime("Arriving By %d %a %B %Y")
    
    order_id = request.session.get('order_id', None)
    date = request.session.get('order_date', None)
    order_status = request.session.get('order_status', None)
    orders = OrderMain.objects.all().order_by('-updated_at')

    return render(request, 'order/order.html',{
        'formatted_future_date': formatted_future_date,
        'order_id': order_id,
        'date': date,
        'order_status': order_status,
        'orders':orders,
    })



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

        if order.payment_option in ["Razorpay", "Wallet Payment"]:
            item_refund = Decimal('0')

            for item in order_items:
                item_amount = Decimal(str(item.price * item.quantity))
                order_amount = Decimal(str(order.total_amount))
                order_discount_amount = Decimal(str(order.discount_amount))

                item_discount_amount = (order_discount_amount * item_amount) / order_amount
                item_refund_amount = item_amount - item_discount_amount

                item_refund += item_refund_amount
                item.is_active = False
                item.main_order.final_amount -= item_refund
                item.save()

            if item_refund > 0:
                description = f"Refund for Cancel order {order.order_id}"
                transaction_type = "Credited"

                wallet, created = Wallet.objects.get_or_create(user=request.user)

                transaction = Transaction.objects.create(
                    wallet=wallet,
                    description=description,
                    amount=item_refund,
                    transaction_type=transaction_type,
                )

                wallet.balance += item_refund  # Ensure Decimal type for accurate calculation
                wallet.save()

            order.final_amount -= item_refund
            order.save()

        
        messages.success(request, 'Order has been successfully canceled.')
        
    except OrderMain.DoesNotExist:
        messages.error(request, 'Order does not exist.')

    return redirect('userdash:user-profile')
        


@admin_required
def admin_cancel_order(request, pk):
    try:
        # Fetch the main order object
        order = get_object_or_404(OrderMain, id=pk)
        # Fetch all active order items related to the main order
        order_items = OrderSub.objects.filter(main_order=order, is_active=True)

        # Loop through order items and update variant stock
        for order_item in order_items:
            order_variant = order_item.variant
            order_quantity = order_item.quantity
            order_variant.variant_stock += order_quantity
            order_variant.save()  # Save the updated stock back to the database

        # Set order status to "Canceled"
        order.order_status = "Canceled"
        order.save()

        refund_amount = Decimal('0.00')

        # Check if the payment option requires a refund
        if order.payment_option in ["Razorpay", "Wallet Payment"]:
            for item in order_items:
                item_total_cost = Decimal(str(item.final_total_cost()))
                order_total_amount = Decimal(str(item.main_order.total_amount))
                order_discount_amount = Decimal(str(item.main_order.discount_amount))

                item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
                item_refund_amount = item_total_cost - item_discount_amount

                refund_amount += item_refund_amount
                item.is_active = False  # Mark order item as inactive
                item.save()

            if refund_amount > 0:
                description = f"Sorry Due To Some Reason Admin Canceled This Order {order.order_id}"
                transaction_type = "Credited"

                # Get or create wallet for the user
                wallet, created = Wallet.objects.get_or_create(user=order.user)

                # Create a transaction
                transaction, created = Transaction.objects.get_or_create(
                    wallet=wallet,
                    description=description,
                    amount=refund_amount,
                    transaction_type=transaction_type,
                )

                # Update the wallet balance
                wallet.balance += refund_amount
                wallet.save()

            # Deduct refund amount from the order's final amount
            order.final_amount -= refund_amount
            order.save()

            # Display success message
            messages.success(request, 'Order Canceled and credited to the user\'s wallet.')
            return redirect('order:admin_orders_details', pk=order.id)

        else:
            # Display success message for non-refundable payment options
            messages.success(request, 'Order Canceled Successfully')
            return redirect('order:admin_orders_details', pk=order.id)

    except OrderMain.DoesNotExist:
        # Handle the case where the order does not exist
        messages.error(request, 'Order does not exist.')
        return redirect('order:admin_orders_details', pk=order.id)

    # # Redirect to order details page if something goes wrong
    # return redirect('admin_panel:admin_order_details', pk=order.id)
            

    

@login_required
def return_order(request, pk):
    if request.method == 'POST':
        try:
            order = get_object_or_404(OrderMain, id=pk)
            order_items = OrderSub.objects.filter(main_order=order)

            if not order.is_active:
                messages.error(request, 'Order item is already returned.')
                return redirect('userdash:user-profile')

            if order.order_status in ['Pending', 'Confirmed', 'Shipped']:
                messages.error(request, 'Order cannot be returned at this stage.')
                return redirect('userdash:user-profile')

            reason = request.POST.get('reason', '').strip()
            if not reason:
                messages.error(request, 'A reason must be provided for returns.')
                return redirect('userdash:user-profile')

            ReturnRequest.objects.create(
                order_main=order,
                reason=reason
            )

            order.order_status = "Pending"
            order.save()

            messages.success(request, "Please wait for the admin's approval.")
            return redirect('userdash:user-profile')

        except OrderMain.DoesNotExist:
            messages.error(request, "Order does not exist.")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('userdash:user-profile')
    else:
        return redirect('userdash:user-profile')
    

@admin_required
def admin_return_requests(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        return_requests = ReturnRequest.objects.filter(order_main__order_id__icontains=search_query).order_by('-created_at')
    else:
        return_requests = ReturnRequest.objects.all().order_by('-created_at')

    # Pagination
    paginator = Paginator(return_requests, 5)  # Show 10 return requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Order/return_request.html', {
        'return_requests': page_obj,
        'search_query': search_query,
    })


@admin_required
def admin_return_approval(request, pk):
    if request.method == 'POST':
        return_request = get_object_or_404(ReturnRequest, id=pk)
        action = request.POST.get('action')
        
        if action == 'Approve':
            return_request.status = "Approved"
            return_request.save()
            
            refund_amount = Decimal('0.00')
            
            if return_request.order_sub:  # If specific item return

                item = return_request.order_sub
                main_order = item.main_order
                item_total_cost = Decimal(str(item.final_total_cost()))
                order_total_amount = Decimal(str(main_order.total_amount))
                order_discount_amount = Decimal(str(main_order.discount_amount))
                
                item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
                refund_amount = item_total_cost - item_discount_amount
                
                item.is_active = False
                item.status = "Returned"
                item.save()
                
                order = return_request.order_main
                order.final_amount -= refund_amount
                order.save()
                
                all_canceled = not main_order.ordersub_set.filter(is_active=True).exists()
                
                if all_canceled:  # If all items are canceled

                    main_order.order_status = 'Returned'
                    main_order.save()
                    
            else:  # If entire order return

                order = return_request.order_main
                active_items = order.ordersub_set.filter(is_active=True)
                
                for item in active_items:
                    item_total_cost = Decimal(str(item.final_total_cost()))
                    order_total_amount = Decimal(str(order.total_amount))
                    order_discount_amount = Decimal(str(order.discount_amount))

                    item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
                    item_refund_amount = item_total_cost - item_discount_amount

                    refund_amount += item_refund_amount
                    item.is_active = False
                    item.status = "Returned"
                    item.save()

                order.order_status = 'Returned'
                order.is_active = False
                order.final_amount -= refund_amount
                order.save()

            if refund_amount > 0 and return_request.order_main.payment_status:
                wallet, created = Wallet.objects.get_or_create(user=return_request.order_main.user)

                wallet.balance += refund_amount
                wallet.updated_at = timezone.now()
                wallet.save()

                Transaction.objects.create(
                    wallet=wallet,
                    amount=float(refund_amount),
                    description=f"Refund for {'order' if return_request.order_sub is None else 'item'} {return_request.order_main.order_id if return_request.order_sub is None else return_request.order_sub.variant.product.product_name}",
                    transaction_type='Credited'
                )
                
                messages.success(request, 'Return request approved and amount credited to the user\'s wallet.')
                return redirect('order:return_requests')
            else:
                messages.success(request, 'Return request approved. No payment was made or payment status is not confirmed.')
                return redirect('order:return_requests')
            
        elif action == "Reject":
            return_request.status = "Rejected"
            if return_request.order_sub:
                return_request.order_sub.status = "Return Rejected"
                return_request.order_sub.save()
            return_request.save()
            messages.success(request, 'Return request rejected.')
            return redirect('order:return_requests')
        
        else:
            messages.error(request, 'Invalid action.')
            return redirect('order:return_requests')

    return redirect('order:return_requests')



@login_required
def individual_cancel(request, pk):
    order_sub = get_object_or_404(OrderSub, id=pk, user=request.user)

    if not order_sub.is_active:
        messages.error(request, 'Order item is already canceled.')
        return redirect('userdash:user-profile')

    if order_sub.main_order.order_status not in ['Pending', 'Confirmed', 'Shipped', 'delivered','Paid']:
        messages.error(request, 'Order cannot be canceled at this stage.')
        return redirect('userdash:user-profile')

    refund_amount = Decimal(0)

    if order_sub.main_order.payment_option in ['Razorpay', 'Wallet Payment']:
        item_total_cost = Decimal(order_sub.total_cost())
        order_total_amount = Decimal(order_sub.main_order.total_amount)
        order_discount_amount = Decimal(order_sub.main_order.discount_amount)

        item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
        refund_amount = item_total_cost - item_discount_amount

        wallet, created = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += refund_amount
        wallet.updated_at = timezone.now()
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=float(refund_amount),
            description=f'Refund for canceled item {order_sub.variant.product.product_name}',
            transaction_type='Credited'
        )

    order_sub.is_active = False
    order_sub.main_order.final_amount -= refund_amount
    order_sub.save()

    all_canceled = not order_sub.main_order.ordersub_set.filter(is_active=True).exists()

    if all_canceled:
        order_sub.main_order.order_status = 'Canceled'
        order_sub.main_order.save()

    order_sub.variant.variant_stock += order_sub.quantity
    order_sub.status = "Canceled"
    order_sub.variant.save()

    messages.success(request, 'Order item canceled successfully.')
    return redirect('userdash:user-profile')




def individual_return(request, pk):
    # Fetch the order item, ensuring the user has access
    order_sub = get_object_or_404(OrderSub, id=pk, user=request.user)

    # Check if the order item has already been returned
    if not order_sub.is_active:
        messages.error(request, 'Order item is already Returned.')
        return redirect('userdash:user-profile')

    # Check if the order status allows for a return
    if order_sub.main_order.order_status in ['Pending', 'Confirmed', 'Shipped', 'Canceled']:
        messages.error(request, 'Order cannot be returned at this stage.')
        return redirect('userdash:user-profile')

    # Get the reason for the return from the POST data
    reason = request.POST.get('reason', '').strip()

    if not reason:
        messages.error(request, 'A reason must be provided for returns.')
        return redirect('userdash:user-profile')

    # Create a return request
    ReturnRequest.objects.create(
        order_main=order_sub.main_order,
        order_sub=order_sub,
        reason=reason
    )

    # Update the order status to "Return Requested"
    order_sub.status = "Return Requested"
    order_sub.save()

    # Notify the user of successful return request submission
    messages.success(request, "Please wait for the admin's approval.")
    return redirect('userdash:user-profile')






@login_required
def razorpay_payment(request):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_total = round(sum(item.sub_total() for item in cart_items), 2)

    coupon_code = request.session.get('applied_coupon')
    print("Coupon Code from Session:", coupon_code)
    discount = 0
    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if cart_total >= coupon.minimum_amount:
                discount = coupon.discount
                discount_amount = (cart_total * discount / 100)
                discount_amount = min(discount_amount, coupon.maximum_amount)
                
                cart_total = cart_total - discount_amount
                request.session['applied_coupon'] = coupon_code
            else:
                messages.error(request, f'Coupon only available for orders over {coupon.minimum_amount}')

        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
    
    new_total = cart_total

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_order = client.order.create({
        'amount': int(new_total * 100),
        'currency': 'INR',
        'payment_capture': '1'
    })
    payment_order_id = payment_order['id']

    context = {
        'cart_total': cart_total,
        'new_total': int(new_total * 100),
        'api_key': settings.RAZORPAY_KEY_ID,
        'order_id': payment_order_id,
        'user_email': current_user.email,
        'user_phone': current_user.profile.phone if hasattr(current_user, 'profile') else '',
    }

    return render(request, 'cart/razorpay.html', context)



@csrf_exempt
def handle_razorpay_payment(request):
    if request.method == "POST":
        try:
            # Parse the received data from the Razorpay handler
            current_user = request.user
            cart = Cart.objects.get(user=current_user)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cart_total = round(sum(item.sub_total() for item in cart_items), 2)
            address = UserAddress.objects.filter(user=current_user, is_deleted=False, order_status=True).first()

            data = json.loads(request.body)
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify the payment
            payment = client.payment.fetch(razorpay_payment_id)
            if payment['status'] == 'captured':
                final_amount = cart_total
                # Handle coupon logic if applicable
                coupon_code = request.session.get('applied_coupon')
                discount = 0
                discount_amount = 0
                if coupon_code:
                    try:
                        
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        if cart_total >= coupon.minimum_amount:
                            discount = coupon.discount
                            discount_amount = (cart_total * discount / 100)
                            discount_amount = min(discount_amount, coupon.maximum_amount)
                            final_amount = cart_total - discount_amount
                        else:
                            messages.error(request, f'Coupon only available for orders over {coupon.minimum_amount}')
                    except Coupon.DoesNotExist:
                        pass

                # Generate order and payment IDs
                user = str(request.user.id)
                current_date_time = datetime.now()
                formatted_date_time = current_date_time.strftime("%H%m%S%Y")
                unique = get_random_string(length=4, allowed_chars='1234567890')
                order_id = user + formatted_date_time + unique

                formatted_date_time = current_date_time.strftime("%m%Y%H%S")
                unique = get_random_string(length=2, allowed_chars='1234567890')
                payment_id = unique + user + formatted_date_time

                # Create an OrderAddress object
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

                # Create the OrderMain object in the database
                order_main = OrderMain.objects.create(
                    user=current_user,
                    address=order_address,
                    total_amount=cart_total,
                    discount_amount=discount_amount,
                    final_amount=final_amount,
                    order_status="Pending",
                    payment_option="Razorpay",
                    payment_status=True,
                    order_id=order_id,
                    payment_id=payment_id
                )

                # Loop through cart items to create OrderSub entries and update stock
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

                # After all items have been processed, delete them from the cart
                cart_items.delete()
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(coupon_code=coupon_code)
                        used_coupon = UserCoupon.objects.create(
                            user = request.user,
                            coupon = coupon,
                            used = True,
                            order = order_main
                        )

                    except Coupon.DoesNotExist:
                        pass
                if "applied_coupon" in request.session:
                        del request.session["applied_coupon"]


                # Update order status to 'Paid' after the order is created
                order_main.order_status = "Paid"
                order_main.save()

                # Return a successful response with redirect URL
                success_url = reverse('order:order_success')
                return JsonResponse({'success': True, 'redirect_url': success_url})
            else:
                # Handle cases where payment is not captured
                return JsonResponse({'success': False, 'message': 'Payment not captured'})

        except OrderMain.DoesNotExist:
            # Handle case where the order does not exist
            return JsonResponse({'success': False, 'message': 'Order does not exist'})

        except Exception as e:
            # Handle general exceptions
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    # Return an error if the request method is not POST
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



@login_required
def applycoupon(request):
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total = sum(item.sub_total() for item in cart_items)
        
        if coupon:
            try:
                coupon_code = Coupon.objects.get(coupon_code=coupon)

                if total > coupon_code.minimum_amount:
                    discount = coupon_code.discount
                    discount_amount = (total * discount / 100)
                    discount_amount = min(discount_amount, coupon_code.maximum_amount)
                    new_total = total - discount_amount

                    # Save coupon code in session
                    request.session['applied_coupon'] = coupon_code.coupon_code
                    request.session.modified = True  # Ensures session is saved
                    
                    # Debugging to ensure session value is set
                    print("Coupon applied:", request.session.get('applied_coupon'))

                    return JsonResponse({
                        'success': True,
                        'new_total': round(new_total, 2),
                        'discount_amount': round(discount_amount, 2),
                        'discount': discount,
                        'message': 'Coupon applied successfully!'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f'Coupon only available for orders over {coupon_code.minimum_amount}'
                    })
            except Coupon.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid coupon code'
                })

        return JsonResponse({
            'success': False,
            'message': 'No coupon code provided'
        })




def removecoupon(request):
    if request.method == 'POST':
        response = {'success': False}

        # Get the user's cart and active cart items
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Remove the applied coupon from the session
        request.session.pop('applied_coupon', None)

        # Calculate the new total after removing the coupon
        new_total = sum(item.sub_total() for item in cart_items)

        # Update the response with success and new total
        response.update({
            'success': True,
            'message': 'Coupon removed successfully.',
            'new_total': round(new_total, 2),
            'discount': 0
        })

        return JsonResponse(response)

