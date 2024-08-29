from django.urls import path
from . import views


app_name = 'userdash'

urlpatterns = [
    path('user-profile/',views.user_profile,name='user-profile'), 
    path('add-address/',views.add_address,name='add-address'),
    path('changepass/',views.changepass,name='changepass'),
    path('edituser/',views.edituser,name='edituser'),
    path('default/<int:pk>/',views.default,name='default'),
    path('delete/<int:pk>/',views.delete,name='delete'),
    path('toggle-address-status/',views.toggle_address_status , name='toggle_address_status'),
    path('add-addresstwo/',views.add_addresstwo,name='add-addresstwo'),
    path('edit_address/<int:pk>/',views.edit_address,name='edit_address'),
    path('search/', views.search, name='search'),
    path('add-to-wishlist/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_wishlist/<int:pk>/',views.remove_wishlist,name='remove_wishlist'),
    path('wishlist-add-to-cart/', views.wishlist_add_to_cart, name='wishlist_add_to_cart'),

]