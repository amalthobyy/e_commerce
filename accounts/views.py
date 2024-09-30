from ast import parse
from datetime import timedelta
import logging
from pyexpat.errors import messages
import random
from time import timezone
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import OtpForm, UserSignup
from .forms import Emailauthentication
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from brand.models import Brand
from product.models import *
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator

# Create your views here.
logger = logging.getLogger(__name__)
User = get_user_model()


def home(request):
    brands = Brand.objects.all()
    products = Products.objects.all()
    return render(request, 'user/home.html',{'brands':brands,'products':products})


def login(request):
    if request.method == 'POST':
        form = Emailauthentication(request, data=request.POST)
        logger.debug(f"Form Valid: {form.is_valid()}")  # Debug statement
        if form.is_valid():
            user = form.get_user()
            logger.debug(f"Authenticated User: {user}")
            if user and user.is_active and not user.is_blocked:
                auth_login(request, user)
                messages.success(request,'successfully loggedin')
                return redirect('accounts:home')
        else:
            messages.error(request,'invalid credentials')
            logger.debug(form.errors)  
    
    form = Emailauthentication()
    return render(request, 'user/login.html', {'form': form})



def signup(request):
    if request.method=='POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user_data = form.save(commit=False)
            user_data.is_active =False
            

            request.session['user_data'] = {
                'first_name': user_data.first_name,
                'last_name' : user_data.last_name,
                'email': user_data.email,
                'password':form.cleaned_data.get('password')
            }

            # Generate and send OTP
            otp = get_random_string(length=6, allowed_chars='1234567890')
            print(otp)
            request.session['otp'] = otp

            subject = 'Your OTP Code'
            message = f'Your OTP code is {otp}'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user_data.email]
            send_mail(subject, message, email_from, recipient_list)

            return redirect('accounts:verify_otp')
    else:
        form = UserSignup()
    return render(request, 'user/register.html',{'form':form})


def verify_otp(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == request.session.get('otp'):
                # OTP is correct, save the user data
                user_data = request.session.get('user_data')
                email = user_data.get('email')
                try:
                    # Check if a user with this email already exists
                    if User.objects.filter(email=email).exists():
                        user = User.objects.get(email=email)
                        messages.warning(request, 'User with this email already exists. Logging you in.')
                    else:
                        user = User.objects.create_user(
                            first_name=user_data.get('first_name'),
                            last_name=user_data.get('last_name'),
                            email=email,
                            password=user_data.get('password'),
                        )
                        user.is_active = True
                        user.save()

                    # Clear the session data
                    del request.session['user_data']
                    del request.session['otp']

                    return redirect('accounts:login')
                except IntegrityError:
                    messages.error(request, 'An error occurred while creating the user. Please try again.')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OtpForm()
    return render(request, 'user/verify_otp.html', {'form': form})


def resend_otp(request):
    user_data = request.session.get('user_data')
    if user_data:
        otp = get_random_string(length=6, allowed_chars='1234567890')
        logger.debug(f"Generated OTP: {otp}")  # Debug statement

        otp_generation_time = timezone.now().isoformat()
        logger.debug(f"OTP Generation Time: {otp_generation_time}")  # Debug statement

        print(otp)

        request.session['otp'] = otp
        request.session['otp_generation_time'] = otp_generation_time

        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user_data['email']],
                fail_silently=False,
            )
            messages.success(request, 'A new OTP has been sent to your email.')
        except Exception as e:
            logger.error(f"Error sending email: {e}")  # Log email sending error
            messages.error(request, 'Failed to send OTP. Please try again later.')
    else:
        messages.error(request, 'User data not found. Please register again.')
    return redirect('accounts:verify_otp')




        

def user(request):
    return render(request, 'user/userdash.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('accounts:home')




def about_us(request):
    return render(request,'info/about-us.html')

def contact_us(request):
    return render(request,'info/contact-us.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "user/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Dripc4rtel',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email_content,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("accounts:password_reset_done")
    
    password_reset_form = PasswordResetForm()
    return render(request, "user/password_reset.html", {"password_reset_form": password_reset_form})


def password_reset_done(request):
    return render(request, 'user/password_reset_done.html')



def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You may go ahead and log in now.')
                return redirect('accounts:password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'user/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link was invalid, possibly because it has already been used. Please request a new password reset.')
        return redirect('accounts:password_reset')
    


def password_reset_complete(request):
    return render(request, 'user/password_reset_complete.html')





def custom_404_view(request, exception):
    return render(request, 'user/404.html', status=404)