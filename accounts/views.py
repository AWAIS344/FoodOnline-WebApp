from django.shortcuts import render
from .models import User
from django.shortcuts import redirect
from django.http import HttpResponse
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
        messages.warning(request,"Your are already LoggedIn!")
        return redirect("myaccount")
    
    form=UserRegForm()
    if request.method == "POST":
        form=UserRegForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.role=User.CUSTOMER
            user.set_password(password)
            user.save()
            send_email_verfication(request,user)
            messages.success(request,"You have successfully Registered!")
            return redirect("register")
        else:
            print(f"Form Issue : {form.errors}")
    else:
        form=UserRegForm()
    
    context={"form":form}
    return render(request,"registration.html",context)


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
    pass


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
