from django.urls import path
from . import views

app_name="admindash"

urlpatterns = [
    path('admin_login/',views.admin_login, name='admin_login'),
    path('admin_home/',views.admin_home, name='admin_home'),
    path('list_user/',views.list_user,name='list_user'),
    path('user_block/<int:user_id>/', views.user_block, name='user_block'),
    path('user_unblock/<int:user_id>/', views.user_unblock, name='user_unblock'),
    path('order_status/<int:pk>/', views.order_status, name='order_status'),
    path('reports/',views.sales_report,name='sales_report'),
    path('filter/',views.order_date_filter,name='date_filter'),
    path('best_selling_products/',views.best_selling_products,name='best_selling_products'),
    path('best_selling_categories/',views.best_selling_categories,name='best_selling_categories'),
    path('best_selling_brands/',views.best_selling_brands,name='best_selling_brands'),
    path('logout/',views.logout,name='admin_logout'),
] 