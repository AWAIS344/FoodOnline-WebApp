from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from accounts.form import UserRegForm
from .form import VendorRegForm
from .models import Vendor
from accounts.form import UserProfileForm
from accounts.models import UserProfile,User
from accounts.utils import send_email_verfication

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
            user.set_password(form.cleaned_data['password'])
            user.save()
            vendor = v_form.save(commit=False)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            vendor.user = user
            vendor.user_profile=user_profile
            vendor.save()
            mail_subject = "FooodOnline Activate Your Acccount"
            email_template="email/forgot_email.html"
            send_email_verfication(request,user,mail_subject,email_template)
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



def Vendor_Profile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)

    if request.method  == 'POST':
        userform=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendorform=VendorRegForm(request.POST,request.FILES,instance=vendor)

        if userform.is_valid() and vendorform.is_valid():
            userform.save()
            vendorform.save()
            messages.success(request,"Profile Successfully Updated")
            return redirect("vendor-profile")
        else:
            messages.error(request,"Please Check Your Info")
            print(userform.erros)
            print(vendorform.errors)
    else:
        userform=UserProfileForm(instance=profile)
        vendorform=VendorRegForm(instance=vendor)
    context={
        "profile":profile,
        "userform":userform,
        "vendorform":vendorform,
        "vendor":vendor,
    }  
    return render(request,"vendor_profile.html",context)