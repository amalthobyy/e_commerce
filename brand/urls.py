from django.urls import path 
from . import views
from . views import *


app_name = 'brand'

urlpatterns = [

  path('brand',views.list_brand,name='list_brand'),
  path('create',views.create_brand,name='create_brand'),
  path('edit/<int:pk>/', EditBrand.as_view(), name='edit_brand'),
  path('delete/<int:pk>/',DeleteBrandView.as_view(),name='delete_brand'),

]