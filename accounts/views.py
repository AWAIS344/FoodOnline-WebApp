from django.shortcuts import render
from .models import User
from django.shortcuts import redirect
from django.http import HttpResponse
from .form import UserRegForm

# Create your views here.


def RegisterUser(request):
    form=UserRegForm()
    if request.method == "POST":
        form=UserRegForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.role=User.CUSTOMER
            user.set_password(password)
            user.save()
            return redirect("register")
        else:
            print(f"Form Issue : {form.errors}")
            form=UserRegForm()
    
    context={"form":form}
    return render(request,"registration.html",context)