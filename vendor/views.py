from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.form import UserRegForm
from .form import VendorRegForm
from accounts.models import UserProfile,User

# Create your views here.
def RegisterVendor(request):
    # form=UserRegForm()
    # v_form=VendorRegForm()
    if request.method =="POST":
        form=UserRegForm(request.POST)
        v_form=VendorRegForm(request.POST,request.FILES)

        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            user.role=User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            vendor.user = user
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,"Your <strong>Restaurent</strong> has successfully Registered! Please wait for Approval - Thanks")
            return redirect("registervendor")

        else:
            print("FORM ISSUE")
            print(form.errors)
            print(v_form.errors)

    else:
        form=UserRegForm()
        v_form=VendorRegForm()
    context={"form":form,"v_form":v_form}    
    return render(request,"registervendor.html",context)