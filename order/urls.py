from django.urls import path 
from . import views


app_name = 'order'

urlpatterns = [
    path('place_order',views.orderverification, name='place_order'),
    path('order_success',views.order_success, name='order_success'),

  
  
]