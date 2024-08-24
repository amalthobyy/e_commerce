from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Products, Category, Brand ,product_image ,Product_Variant, product_image 
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Products, Review
from django.db.models import Avg, Count, Sum, Prefetch
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.


class ListProduct(View):
    def get(self,request):
        products =Products.objects.all()
        return render(request, 'admindash/list_product.html',{'products':products})

class ProductDetailView(View):
    def get(self,request,product_id):
        products= get_object_or_404(Products,id =product_id)  
        images = product_image.objects.filter(product = products)
        return render(request,'admindash/product_detail.html',{'products':products,'images':images})


class CreateProductView(View):
    def get(self,request):
        categories = Category.objects.all()
        brands = Brand.objects.all()
        return render(request, 'admindash/create_product.html', {'categories': categories, 'brands': brands})
    

    def post(self,request):
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_description = request.POST.get('product_description')
            product_category_id = request.POST.get('product_category')
            product_brand_id = request.POST.get('product_brand')
            price = request.POST.get('price')
            offer_price = request.POST.get('offer_price')
            is_active = request.POST.get('is_active') == 'on'
            thumbnail = request.FILES.get('thumbnail')

            product_category = Category.objects.get(id=product_category_id) if product_category_id else None
            product_brand = Brand.objects.get(id=product_brand_id) if product_brand_id else None

            product = Products.objects.create(
            product_name=product_name,
            product_description=product_description,
            product_category=product_category,
            product_brand=product_brand,
            price=price,
            offer_price=offer_price,
            thumbnail=thumbnail,
            is_active=is_active,
            )

            return redirect('product:list_product')
        
        
    
def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if request.method == 'POST':
        product = get_object_or_404(Products, id=product_id)
        product.product_name = request.POST.get('product_name')
        product.product_description = request.POST.get('product_description')
        product_category_id = request.POST.get('product_category')
        product_brand_id = request.POST.get('product_brand')
        product.price = request.POST.get('price')
        product.offer_price = request.POST.get('offer_price')
        product.is_active = request.POST.get('is_active') == "on"

        if request.FILES.get('thumbnail'):
            product.thumbnail = request.FILES.get('thumbnail')

        if request.FILES.get('thumbnail_hover'):
            product.thumbnail_hover = request.FILES.get('thumbnail_hover')
    

        product.product_category = Category.objects.get(id=product_category_id) if product_category_id else None
        product.product_brand = Brand.objects.get(id=product_brand_id) if product_brand_id else None

        product.save()
        return redirect('product:product-detail', product_id=product_id)

    return render(request, 'admindash/edit_product.html', {'product': product, 'categories': categories, 'brands': brands})



def product_status(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    product.is_active = not product.is_active
    product.save()
    return redirect('product:product-detail',product_id=product_id)


def add_images(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        thumbnail = request.FILES.get('thumbnail')
        images = request.FILES.getlist('images')
        
        if thumbnail:
            product.thumbnail = thumbnail
            product.save()

        for image in images:
            product_image.objects.create(product=product, images=image)

        return redirect('product:product-detail',product_id=product_id)

    return render(request, 'admindash/add_images.html', {'product': product})



def add_variant(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    variants = Product_Variant.objects.filter(product=product)
    
    if request.method == 'POST':
        size = request.POST.get('size')
        variant_stock = request.POST.get('variant_stock')
        variant_status = request.POST.get('variant_status') == 'on'
        
        if Product_Variant.objects.filter(product=product, size=size).exists():
            messages.error(request, 'A variant with this size already exists for this product.')
            return render(request, 'admindash/add_variant.html', {'product': product})

       
        
        variant = Product_Variant.objects.create(
            product=product,
            size=size,
           
            variant_stock=variant_stock,
            variant_status=variant_status,
           
        )

        return redirect('product:variant-detail', product_id=product.id)  

    return render(request, 'admindash/add_variant.html', {'product': product,})


   




def variant_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    
    variants = Product_Variant.objects.filter(product=product)
    context = {
        'product': product,
        'variants': variants,
    }
    return render(request, 'admindash/variant_detail.html', context)


def variant_status(request, variant_id):
    variant = get_object_or_404(Product_Variant, id=variant_id)
    variant.variant_status = not variant.variant_status
    variant.save()
    return redirect('product:variant-detail', variant.product.id)




def edit_variant(request, variant_id):
    variant = get_object_or_404(Product_Variant, id=variant_id)
   
    if request.method == 'POST':
        variant = get_object_or_404(Product_Variant, id=variant_id)
        
        variant.size = request.POST.get('variant_size')
        variant.variant_stock = request.POST.get('variant_stock')
        variant.variant_status = request.POST.get('variant_status') == 'on'

      
        variant.save()
        return redirect('product:variant-detail', variant.product.id)
    
    return render(request, 'admindash/edit_variant.html', {'variant': variant})

def product_images(request,pk):
    if request.method =="POST":
        product=Products.objects.get(id=pk)
        images=request.FILES.getlist('images')

        for image in images:
            product_image.objects.create(product=product,images=image)
        
        return redirect('product:product-detail',product_id = product.id)
    product = get_object_or_404(Products, id=pk)
    return render(request, 'admindash/add_productimg.html',{'product':product})


def remove(request,pk):
    image=product_image.objects.get(id=pk)
    image.delete()
    pk=image.product.id
    return redirect('product:product-detail',product_id=pk)



#----------userside--------------
def shop_page(request):
    sort_by = request.GET.get('SortBy')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    
    sort_options = {
        'title-ascending': 'product_name',
        'title-descending': '-product_name',
        'price-low-to-high': 'price',
        'price-high-to-low': '-price',
        'best-selling': '-sales',  # ensure you have a 'sales' field
        'average-ratings': '-average_rating',  # ensure you have an 'average_rating' field
        'popularity': '-popularity'  # ensure you have a 'popularity' field
    }

    if sort_by in sort_options:
        sort_field = sort_options[sort_by]
        products = Products.objects.all().order_by(sort_field)
    elif brand:
        products=Products.objects.filter(product_brand__brand_name=brand)   

    elif category:
        products = Products.objects.filter(product_category__slug=category)

    else:
        products = Products.objects.all()
    
    count = products.count()

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'user/product/shop_page.html',{'products':products, 'categories':categories, 'brands':brands,'count':count})



def product_details(request,pk):
    
    products = Products.objects.get(id=pk)
    variants = Product_Variant.objects.filter(product=products)
    reviews = Review.objects.filter(product= products)
    images = product_image.objects.filter(product=products)
    return render(request,'user/product/product_details.html',{'products':products,'reviews':reviews,'images':images,'variants':variants})

def product_reviews(request):

    return render(request,'user/product/product_details.html')


def review(request,pk):
    product = get_object_or_404(Products, id=pk)
    pk=product.id
    if request.method=="POST":
        rating=request.POST.get('rating')
        review=request.POST.get('review')

        Review.objects.create(user=request.user,product=product,rating=rating,comment=review)

    return redirect('product:product-detailsuser',pk=pk)