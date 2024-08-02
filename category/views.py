from django.shortcuts import render,redirect,get_object_or_404
from .models import Category
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.



def list_category(request):
    categories = Category.objects.all().order_by('id')
    return render(request,'admindash/list_category.html',{'categories':categories})



def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        try:
            category = Category.objects.create(category_name=category_name)
            messages.success(request, f'Category "{category_name}" created successfully.')
            return redirect('category:list-category')
        except IntegrityError:
            messages.error(request, f'Category "{category_name}" already exists.')
            return render(request, 'admindash/create_category.html')
        except Exception as e:
            messages.error(request, f'Failed to create category: {str(e)}')
            return render(request, 'admindash/create_category.html')

    return render(request, 'admindash/create_category.html')




def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
            messages.error(request, 'Category with this name already exists.')
        else:    
            category.category_name = category_name
            category.slug = slug
            category.save()
            return redirect('category:list-category')
    return render(request, 'admindash/edit_category.html', {'category': category})



def category_is_available(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.is_available = not category.is_available
    category.save()
    return redirect('category:list-category')

