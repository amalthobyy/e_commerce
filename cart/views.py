from django.shortcuts import render,redirect
from django.http import JsonResponse

from product.models import * 




def add_to_cart(request):
    print("Add to cart view called")
    if request.method =="POST":
        product= request.POST.get('product_id')
        variant=request.POST.get('variant_id')
        print(product)
        print(variant)
        return redirect('accounts:home')


        # products = Products.objects.get(id=pk)
        # variants = Product_Variant.objects.get()




