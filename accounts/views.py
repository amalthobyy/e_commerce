from django.shortcuts import render

# Create your views here.


def home(request):


    return render (request ,'user/home.html')



def login(request):
    return render(request,'user/login.html')


def signup(request):
    return render(request, 'user/register.html')

def con(request):
    return render(request, 'conus.html')


def user(request):
    return render(request, 'user/userdash.html')