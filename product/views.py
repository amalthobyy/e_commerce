from django.shortcuts import get_object_or_404, render
from django.views import View
from dripdeck.product.models import* 

# Create your views here.


class ListProductView(View):
    def get(self,request):
        products =Products.objects.all()
        return render(request, 'admindash/list_product.html',{'produts':products})

class ProductDetailView(View):
    def get(self,request,product_id):
        products= get_object_or_404(Products,id =product_id)  
        images = product_image.objects.filter(product = products)
        return render(request,'admindash/product_deatil.html',{'products':products,'images':images})
    