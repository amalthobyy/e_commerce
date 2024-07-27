from django.urls import path 
from . import views


app_name = 'category'

urlpatterns = [

  path('list-category',views.list_category,name='list-category'),
  path('create-category',views.create_category,name='create-category'),
  path('edit-category/<int:category_id>/', views.edit_category, name='edit-category'),
  path('available-category/<int:category_id>/',views.category_is_available,name='available-category'),
]