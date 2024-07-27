from django.urls import path
from . import views

app_name="admindash"

urlpatterns = [
    path('admin_login/',views.admin_login, name='admin_login'),
    path('admin_home/',views.admin_home, name='admin_home'),
    path('list_user/',views.list_user,name='list_user'),
    path('user_block/<int:user_id>/', views.user_block, name='user_block'),
    path('user_unblock/<int:user_id>/', views.user_unblock, name='user_unblock'),
]