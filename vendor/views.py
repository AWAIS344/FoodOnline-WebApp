from django.shortcuts import render
from accounts.form import UserRegForm
from .form import VendorRegForm

# Create your views here.
def RegisterVendor(request):
    # form=UserRegForm()
    # v_form=VendorRegForm()
    if request.method =="POST":
        form=UserRegForm(request.POST)
        v_form=VendorRegForm(request.POST,request.FILES)

        if form.is_valid() and v_form.is_valid():
            

        else:
            print("FORM ISSUE")
            print(form.errors)
            print(v_form.errors)

    else:
        form=UserRegForm()
        v_form=VendorRegForm()
    context={"form":form,"v_form":v_form}    
    return render(request,"registervendor.html",context)