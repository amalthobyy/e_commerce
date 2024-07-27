from django.urls import path 
from . import views

app_name = 'product'

urlpatterns = [
    path('list/',views.ListProductView.as_view,name='list_product'),
    path('detail/',views.ProductDetailView.as_view,name='product_detail')
    
    
]