from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('user/',views.user,name='user'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp',views.resend_otp,name='resend_otp'),
    path('logout',views.logout,name='logout'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
