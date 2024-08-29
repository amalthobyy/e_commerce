from django.urls import path
from . views import *
from . import views

app_name = 'coupon'

urlpatterns = [
    path('create_coupon/',views.create_coupon,name='create_coupon'),
     path('coupon/',views.coupon_list, name='coupon'),
     path('edit_coupon/<int:pk>/',views.edit_coupon, name='edit_coupon'),
     path('coupon_status/<int:pk>/',views.toggle_coupon_status, name='coupon_status')
]