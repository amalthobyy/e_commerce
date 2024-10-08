from django.urls import path
from . views import *
from . import views


app_name = 'cart'

urlpatterns = [
    path('add_to_cart',views.add_to_cart, name='add_to_cart'),
    path('list_cart/',views.list_cart, name='list_cart'),
    path('update_is_active/', views.update_is_active, name='update_is_active'),
    path('update-quantity/',views.update_cart_quantity, name='update_cart_quantity'),
    path('cart_checkout/',views.cart_checkout, name='cart_checkout'),
    path('remove_item_cart/<int:pk>/',views.remove_item_cart, name='remove_item_cart'),
    # path('apply-coupon/',views.apply_coupon, name='apply_coupon'),
    # path('remove-coupon/',views.remove_coupon, name='remove_coupon'),
]