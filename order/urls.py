from django.urls import path 
from . import views


app_name = 'order'

urlpatterns = [
    path('place_order/',views.orderverification, name='place_order'),
    path('order_success/',views.order_success, name='order_success'),
    path('list_order_admin/',views.list_order_admin, name='list_order_admin'),
    path('admin_orders_details/<int:pk>/',views.admin_orders_details, name='admin_orders_details'),
    path('cancel_order/<int:pk>/',views.cancel_order, name='cancel_order'),
    path('razorpay-payment/', views.razorpay_payment, name='razorpay_payment'),
  
]