from django.urls import path

from .import views
from .views import CreateProductView, ListProduct, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('list/', ListProduct.as_view(), name='list_product'),
    path('detail/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('edit/<int:product_id>',views.edit_product,name='edit-product'),
    path('status/<int:product_id>',views.product_status,name='product-status'),
    path('add-images/<int:product_id>',views.add_images,name='add-images'),
    path('add-variant/<int:product_id>',views.add_variant,name='add-variant'),
    path('variant/<int:product_id>/', views.variant_detail, name='variant-detail'),
    path('edit-variant/<int:variant_id>/',views.edit_variant, name='edit-variant'),
    path('variant-status/<int:variant_id>/',views.variant_status, name='variant-status'),
    path('product_images/<int:pk>/',views.product_images, name='product_images'),
    path('remove_images/<int:pk>/',views.remove, name='remove_images'),
    path('shop-page',views.shop_page, name='shop-page'),
    path('product-details/<int:pk>/', views.product_details, name='product-detailsuser'),
    path('review/<int:pk>',views.review, name='review'),
]
