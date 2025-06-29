from django.shortcuts import render
from .models import User
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from .form import UserRegForm
from vendor.models import Vendor
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
                messages.error(request, "Invalid email address. Please enter a valid email OR check for typo.")
                return render(request, "registration.html", {"form": form})

            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()

            mail_subject = "FooodOnline Activate Your Acccount"
            email_template="email/forgot_email.html"
            send_email_verfication(request,user,mail_subject,email_template)
            messages.success(request, "You have successfully Registered! Please check you email if not check your spam folder")
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
        user = User._default_manager.get(pk=uid)
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


def Forgot_Password(request):
    if request.method == "POST":
        email=request.POST["email"]
        if User.objects.filter(email__exact=email):
            user=User.objects.get(email=email)



            #Custom Helper Function
            mail_subject = "FooodOnline Forgot Password"
            email_template="email/forgot_email.html"
            send_email_verfication(request,user,mail_subject,email_template)
            messages.success(request, "Link Sent! Please check your email")
        else:
            messages.error(request, "Check your Email or Try Again - Error While Fetching the Account")

            return redirect("forgot_password")

    return render(request,"forgot_password.html")

def Reset_Password_Validate(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,User.DoesNotExist,OverflowError):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        return redirect("reset_password")
    else:
        messages.error(request,"This Link Has Been Expired")
        redirect("myaccount")

def Reset_Password(request):
    if request.method == 'POST':
        password=request.POST["password"]
        confirm_password=request.POST['confirm_password']

        if password == confirm_password:
            pk=request.session.get("uid")
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            mail_subject = "FooodOnline Password Successfully Reset"
            email_template="email/password_email.html"
            send_email_verfication(request,user,mail_subject,email_template)
            messages.success(request,"Password Successfully Reset")
            return redirect('login')
        else:
            messages.error(request,"Both the Password should match")
            return redirect("reset_password")
    return render(request,"reset_password.html")
    
