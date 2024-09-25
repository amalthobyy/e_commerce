from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .models import Brand
from django.contrib import messages


# Create your views here.


def list_brand(request):
    brand = Brand.objects.all().order_by('id')
    return render(request, 'admindash/list_brand.html', {'brand': brand})


def create_brand(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brand_image = request.FILES.get('brand_image')
        status = request.POST.get('status') == "True"

        Brand.objects.create(
            brand_name=brand_name,
            brand_image=brand_image,
            is_active=status,
        )

        return redirect('brand:list_brand')

    return render(request, 'admindash/create_brand.html')


class EditBrand(View):
    def get(self, request, pk):
        brand = Brand.objects.get(id=pk)
        return render(request, 'admindash/edit_brand.html', {'brand': brand})

    def post(self, request, pk):
        brand = Brand.objects.get(id=pk)
        brand.brand_name = request.POST.get('brand_name')
        brand.brand_image = request.FILES.get('brand_image')
        brand.is_active = request.POST.get('status')

        brand.save()
        messages.success(request,'Brand edited succesfuly')
        return redirect('brand:list_brand')


class DeleteBrandView(View):
    def post(self, request, pk):
        brand = Brand.objects.get(id=pk)
        brand.is_active = not brand.is_active
        brand.save()
        return redirect('brand:list_brand')
