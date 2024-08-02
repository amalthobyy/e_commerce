from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Products, Category, Brand ,product_image ,Product_Variant,Product_variant_images, product_image 
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
            product.save()

            return redirect('product:list_product')
        
        
    
def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.product_description = request.POST.get('product_description')
        product_category_id = request.POST.get('product_category')
        product_brand_id = request.POST.get('product_brand')
        product.price = request.POST.get('price')
        product.offer_price = request.POST.get('offer_price')

        if request.FILES.get('thumbnail'):
            product.thumbnail = request.FILES.get('thumbnail')
        product.is_active = request.POST.get('is_active') == 'on'

        if request.FILES.get('thumbnail_hover'):
            product.thumbnail_hover = request.FILES.get('thumbnail_hover')
    

        product.product_category = Category.objects.get(id=product_category_id) if product_category_id else None
        product.product_brand = Brand.objects.get(id=product_brand_id) if product_brand_id else None

        product.updated_at = timezone.now()  # Update the updated_at timestamp
        product.save()
        return redirect('product:product-detail', product_id=product_id)

    categories = Category.objects.all()
    brands = Brand.objects.all()
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
        colour_name = request.POST.get('colour_name')
        variant_stock = request.POST.get('variant_stock')
        variant_status = request.POST.get('variant_status') == 'on'
        colour_code = request.POST.get('colour_code')

        if Product_Variant.objects.filter(product=product, colour_name=colour_name, colour_code=colour_code).exists():
            messages.error(request, "A variant with this color name and color code already exists.")
            return redirect('product:add-variant', product_id=product_id)
        
        variant = Product_Variant.objects.create(
            product=product,
            size=size,
            colour_name=colour_name,
            variant_stock=variant_stock,
            variant_status=variant_status,
            colour_code=colour_code
        )

        return redirect('product:add-variant-image', product_variant_id=variant.id)  

    return render(request, 'admindash/add_variant.html', {'product': product, 'variants': variants})


def add_variant_image(request, product_variant_id):
    product_variant = get_object_or_404(Product_Variant, id=product_variant_id)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        
        if images:
            for image in images:
                Product_variant_images.objects.create(product_variant=product_variant, images=image)
            return redirect('product:variant-detail', product_id=product_variant.product.id)
        
        return HttpResponse("Invalid data", status=400)

    return render(request, 'admindash/add_variant_image.html', {'product_variant': product_variant})


def delete_image(request, image_id):
    if request.method == 'DELETE':
        print('hlo')
        try:
            image = Product_variant_images.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except Product_variant_images.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def variant_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    
    variants = Product_Variant.objects.filter(product=product).prefetch_related('product_variant_images_set')
    
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
    variant_images = Product_variant_images.objects.filter(product_variant=variant)
    
    if request.method == 'POST':
        variant.size = request.POST.get('variant_size')
        variant.colour_name = request.POST.get('colour_name')
        variant.colour_code = request.POST.get('colour_code')
        variant.variant_stock = request.POST.get('variant_stock')
        variant.variant_status = request.POST.get('variant_status') == 'on'

        if request.FILES.get('images'):
            Product_variant_images.objects.create(
                product_variant=variant,
                images=request.FILES.get('images')
            )
        
        variant.save()
        return redirect('product:variant-detail', variant.product.id)
    
    return render(request, 'admindash/edit_variant.html', {'variant': variant,'variant_images': variant_images,})


def shop_page(request):
    products = Products.objects.all()
    return render(request, 'user/product/shop_page.html',{'products':products})



def product_details(request,pk):
    products = Products.objects.get(id=pk)
    
    return render(request,'user/product/product_details.html',{'products':products})