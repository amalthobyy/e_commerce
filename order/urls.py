from django.urls import path 
from . import views


app_name = 'order'

urlpatterns = [
    path('place_order/',views.orderverification, name='place_order'),
    path('order_success/',views.order_success, name='order_success'),
    path('list_order_admin/',views.list_order_admin, name='list_order_admin'),
    path('admin_orders_details/<int:pk>/',views.admin_orders_details, name='admin_orders_details'),
    path('cancel_order/<int:pk>/',views.cancel_order, name='cancel_order'),
    path('return_order/<int:pk>/',views.return_order, name='return_order'),
    path('razorpay-payment/', views.razorpay_payment, name='razorpay_payment'),
    path('razorpay-handler/', views.handle_razorpay_payment, name='handle_razorpay_payment'),
    path('applycoupon/', views.applycoupon, name='applycoupon'),
    path('return_requests/',views.admin_return_requests, name='return_requests'),
    path('admin_return_approval/<int:pk>/',views.admin_return_approval, name='admin_return_approval'),
    path('admin_cancel_order/<int:pk>/',views.admin_cancel_order, name='admin_cancel_order'),
    path('individual_cancel/<int:pk>/',views.individual_cancel, name='individual_cancel'),
    path('individual_return/<int:pk>/',views.individual_return, name='individual_return'),
    path('removecoupon/', views.removecoupon, name='removecoupon'),
  
]