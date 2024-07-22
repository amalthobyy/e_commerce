from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('con',views.con,name='con'),
    path('user',views.user,name='user'),
]
