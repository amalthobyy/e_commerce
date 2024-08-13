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
]