from django.shortcuts import render
from .models import User
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from .form import UserRegForm
from django.contrib import messages,auth
from.utils import detectuser,send_email_verfication
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.

def user_check(required_role):
    def inner(user):
        return user.is_authenticated and user.role == required_role
    return inner


def RegisterUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged In!")
        return redirect("myaccount")

    form = UserRegForm()
    
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Email validation
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Invalid email address. Please enter a valid email.")
                return render(request, "registration.html", {"form": form})

            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()

            send_email_verfication(request, user)
            messages.success(request, "You have successfully Registered! Please check your email for verification.")
            return redirect("register")
        else:
            print(f"Form Error: {form.errors}")
    
    return render(request, "registration.html", {"form": form})


def login(request):

    if request.user.is_authenticated:
        messages.warning(request,"Your are already LoggedIn!")
        return redirect("myaccount")

    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You have Successfully Loggedin!")
            return redirect("myaccount")
        else:
            messages.error(request,"Invalid Credentials")
        
    return render(request,"login.html",)

def logout(request):
    auth.logout(request)
    messages.info(request,"You have Successfully Logout")
    return redirect("login")


def Activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager(pk=uid)
    except(TypeError,ValueError,User.DoesNotExist,OverflowError):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Your Account has Successfully Activated!')
        return redirect("myaccount")
    else:
        messages.error(request,"Invalid Activation Link")
        return redirect("myaccount")


@login_required(login_url="login")
def MyAccount(request):
    user=request.user
    user_url = detectuser(user)
    return redirect(user_url)


@login_required(login_url="login")
@user_passes_test(user_check(1))
def Vend_dashboard(request):
    return render(request,"vend_dashboard.html",)


@login_required(login_url="login")
@user_passes_test(user_check(2))
def Cust_dashboard(request):
    return render(request,"cust_dashboard.html",)
