from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from accounts.form import UserRegForm
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import user_check
from .form import VendorRegForm
from .models import Vendor
from accounts.form import UserProfileForm
from accounts.models import UserProfile,User
from accounts.utils import send_email_verfication
from menu.models import Catagory,FoodItems

from menu.form import CatagoryForm,FoodItemsForm
from django.utils.text import slugify


def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor
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



@login_required(login_url="login")
@user_passes_test(user_check(1))
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



@login_required(login_url="login")
@user_passes_test(user_check(1))
def Menu_Builder(request):
    vendor=get_vendor(request)
    catagories=Catagory.objects.filter(vendor=vendor)
    context={
        "catagories":catagories
    }
    return render(request,"menu_builder.html",context)



@login_required(login_url="login")
@user_passes_test(user_check(1))
def Food_Item_By_Catagory(request,pk=None):
    vendor=get_vendor(request)
    catagories=get_object_or_404(Catagory,pk=pk)
    fooditems=FoodItems.objects.filter(catagory=catagories,vendor=vendor)

    context={
        "fooditems":fooditems,
        "catagories":catagories,
    }
    return render(request,"food_item_by_cat.html",context)


def Add_Catagory(request):

    if request.method == "POST":
       
        form=CatagoryForm(request.POST)
        if form.is_valid():
            catagory_name=form.cleaned_data['catagory_name']
            catagory=form.save(commit=False)
            catagory.vendor=get_vendor(request)
            catagory.slug=slugify(catagory_name)
            form.save()
            messages.success(request,"Category Successfully Added")
            return redirect("menu-builder")
    else:
        form=CatagoryForm()
    context={
        "form":form
    }
    return render(request,"add_catagory.html",context)


def Edit_Catagory(request, pk=None):
    catagory = get_object_or_404(Catagory, pk=pk)

    if request.method == "POST":
        form = CatagoryForm(request.POST, instance=catagory)
        if form.is_valid():
            catagory = form.save(commit=False)
            catagory_name = form.cleaned_data['catagory_name']
            catagory.slug = slugify(catagory_name)
            catagory.vendor = get_vendor(request)
            catagory.save()
            messages.success(request, "Category successfully updated.")
            return redirect("menu-builder")
    else:
        form = CatagoryForm(instance=catagory)

    context = {
        "form": form,
        "catagory": catagory 
    }
    return render(request, "edit_catagory.html", context)


def Delete_Catagory(request,pk=None):
    catagory=get_object_or_404(Catagory,pk=pk)
    catagory.delete()
    messages.success(request, "Category successfully Deleted.")
    return redirect("menu-builder")
    



def Add_Fooditem(request):
    if request.method == "POST":
        form=FoodItemsForm(request.POST,request.FILES)
        if form.is_valid():
            food_title=form.cleaned_data['title']
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(food_title)
            food.save()
            messages.success(request,"Food Item Successfully Added")
            return redirect("menu-builder")
        else:
            print(form.errors)
    else:
        form=FoodItemsForm()
        form.fields['catagory'].queryset = Catagory.objects.filter(Vendor=get_vendor(request))
    context={
        "form":form
    }
    return render(request,"add_food.html",context)


def Edit_Food(request,pk=None):
    food=get_object_or_404(FoodItems,pk=pk)

    if request.method == "POST":
        form = FoodItemsForm(request.POST, request.FILES,instance=food)
        if form.is_valid():
            food=form.save(commit=False)
            food_title=form.cleaned_data['title']
            food.vendor=get_vendor(request)
            food.slug=slugify(food_title)
            food.save()
            messages.success(request,"Food Item Successfully Updated")
            return redirect("menu-builder")
        else:
            print(form.errors)
    else:
        form=FoodItemsForm(instance=food)
    context={
        "form":form,
        "food":food
    }
    return render(request,"edit_food.html",context)


def Delete_Food(request,pk=None):
    food=get_object_or_404(FoodItems,pk=pk)
    food.delete()
    messages.success(request, "Food successfully Deleted.")
    return redirect("menu-builder")
    




