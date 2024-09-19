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
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('password-reset/',views.password_reset_request, name='password_reset'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]
