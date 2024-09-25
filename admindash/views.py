from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import User 
from order.models import *
from utils.decorators import admin_required
from django.db.models.functions import ExtractMonth, ExtractYear, TruncMonth
import json
from django.db.models import Sum, Count, F, Q
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout




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
    # Total order amount
        total_order_amount = OrderMain.objects.filter(order_status="Order Placed").aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Total order count
        total_order_count = OrderMain.objects.filter(order_status="Order Placed").aggregate(total_orders=Count('id'))['total_orders'] or 0
        
        # Total discount
        total_discount = OrderMain.objects.filter(order_status="Order Placed").aggregate(
            total_discount=Sum(F('discount_amount'))
        )['total_discount'] or 0
        
        # Monthly earnings
        now = timezone.now()
        current_year = now.year
        current_month = now.month
        
        monthly_earnings = OrderMain.objects.filter(
            order_status="Order Placed",
            date__year=current_year,
            date__month=current_month
        ).aggregate(monthly_total=Sum('total_amount'))['monthly_total'] or 0

        # Data for the order chart
        monthly_order_count = OrderMain.objects.filter(
            order_status="Order Placed"
        ).annotate(
            month=ExtractMonth('date'),
            year=ExtractYear('date')
        ).values('year', 'month').annotate(count=Count('id')).order_by('year', 'month')

        labels = [f'{entry["month"]}/{entry["year"]}' for entry in monthly_order_count]
        data = [entry['count'] for entry in monthly_order_count]

        # User registration data
        user_registrations = User.objects.annotate(
            month=TruncMonth('date_joined')
        ).values('month').annotate(count=Count('id')).order_by('month')

        user_labels = [entry['month'].strftime('%b %Y') for entry in user_registrations]
        user_data = [entry['count'] for entry in user_registrations]

        context = {
            'total_order_amount': total_order_amount,
            'total_order_count': total_order_count,
            'total_discount': total_discount,
            'monthly_earnings': monthly_earnings,
            'labels': json.dumps(labels),
            'data': json.dumps(data),
            'user_labels': json.dumps(user_labels),
            'user_data': json.dumps(user_data)
        }
        
        return render(request,'admindash/admin_dash.html',context)


def sales_report(request):
    filter_type = request.GET.get('filter', None)
    now = timezone.now()
    start_date = end_date = None  # Initialize to None

    if filter_type == 'weekly':
        start_date = now - timedelta(days=now.weekday())
        end_date = now
    elif filter_type == 'monthly':
        start_date = now.replace(day=1)
        end_date = now

    # Filter orders based on whether a date range is defined
    if start_date and end_date:
        orders = OrderMain.objects.filter(
            order_status="Order Placed",
            is_active=True,
            date__range=[start_date, end_date]
        )
    else:
        # No specific filter, show all "Order Placed" orders
        orders = OrderMain.objects.filter(
            order_status="Order Placed",
            is_active=True
        )

    total_discount = orders.aggregate(total=Sum('discount_amount'))['total']
    total_orders = orders.aggregate(total=Count('id'))['total']
    total_order_amount = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    return render(request, 'admindash/sales_report.html', {
        'orders': orders,
        'total_discount': total_discount,
        'total_orders': total_orders,
        'total_order_amount': total_order_amount
    })

def order_date_filter(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return redirect('admin_panel:sales_report')

            orders = OrderMain.objects.filter(
                date__range=[start_date, end_date], 
                order_status="Order Placed"
            )
            total_discount = orders.aggregate(total=Sum('discount_amount'))['total']
            total_orders = orders.aggregate(total=Count('id'))['total']
            total_order_amount = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

            return render(request, 'admindash/sales_report.html', {
                'orders': orders,
                'total_discount': total_discount,
                'total_orders': total_orders,
                'total_order_amount': total_order_amount
            })

    return redirect('admindash:sales_report')
    

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




def best_selling_products(request):
    best_selling_products = OrderSub.objects.filter(
        main_order__order_status="Order Placed"
    ).values(
        'variant__product__id',
        'variant__product__product_name'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')
    
    top_product = best_selling_products.first()

    return render(request, 'admindash/best_selling_product.html', {
        'top_product': top_product,
        'best_selling_products': best_selling_products
    })


def best_selling_categories(request):
    best_selling_categories = OrderSub.objects.filter(
        main_order__order_status="Order Placed"
    ).values(
        'variant__product__product_category__id',
        'variant__product__product_category__category_name',
        'variant__product__thumbnail'  # Include the thumbnail
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')
    
    top_category = best_selling_categories.first()

    return render(request, 'admindash/best_selling_category.html', {
        'top_category': top_category,
        'best_selling_categories': best_selling_categories
    })


def best_selling_brands(request):
    best_selling_brands = OrderSub.objects.filter(
        main_order__order_status="Order Placed"
    ).values(
        'variant__product__product_brand__id',
        'variant__product__product_brand__brand_name',
        'variant__product__product_brand__brand_image'  # Include brand image
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')

    top_brand = best_selling_brands.first()

    return render(request, 'admindash/best_selling_brand.html', {
        'top_brand': top_brand,
        'best_selling_brands': best_selling_brands
    })


def logout(request):
    auth_logout(request)
    return redirect('admindash:admin_login') 