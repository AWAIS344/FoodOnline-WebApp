from django.shortcuts import render
from .models import User
from django.shortcuts import redirect
from django.http import HttpResponse
from .form import UserRegForm
from django.contrib import messages,auth

# Create your views here.


def RegisterUser(request):

    if request.user.is_authenticated:
        messages.warning(request,"Your are already LoggedIn!")
        return redirect("dashboard")
    
    form=UserRegForm()
    if request.method == "POST":
        form=UserRegForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.role=User.CUSTOMER
            user.set_password(password)
            user.save()
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
        return redirect("dashboard")

    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You have Successfully Loggedin!")
            return redirect("dashboard")
        else:
            messages.error(request,"Invalid Credentials")
        
    return render(request,"login.html",)

def logout(request):
    auth.logout(request)
    messages.info(request,"You have Successfully Logout")
    return redirect("login")


# def MyAccount(request):
#     pass

# def MyAccount(request):
#     pass
# def Vend_dashboard(request):
#     return render(request,"dashboard.html",)

# def Cust_dashboard(request):
#     return render(request,"dashboard.html",)

def dashboard(request):
    return render(request,"dashboard.html",)