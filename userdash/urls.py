from django.urls import path
from . import views


app_name = 'userdash'

urlpatterns = [
    path('user-profile/',views.user_profile,name='user-profile'), 
    path('add-address/',views.add_address,name='add-address'),
]