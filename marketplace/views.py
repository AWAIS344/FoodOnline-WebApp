from django.shortcuts import render,get_object_or_404
from vendor.models  import Vendor
from menu.models import Catagory,FoodItems
from django.db.models import Prefetch


# Create your views here.

def Marketplace(request):
    vendor=Vendor.objects.filter(is_approved=True,user__is_active=True)[:8].prefetch_related('categories')
    vendor_count=vendor.count()
    context={
        "vendor_count":vendor_count,
        "vendor":vendor
    }
    return render(request,"marketplace.html",context)



def Detail_Page(request,vendor_slug):

    vendor=get_object_or_404(Vendor.objects,vendor_slug=vendor_slug)

    catagory=Catagory.objects.filter(vendor=vendor).prefetch_related(Prefetch("fooditems",queryset=FoodItems.objects.filter(is_available=True),to_attr='available_foods'))

    context={
        "vendor":vendor,
        "catagory":catagory,
    }
    return render(request,"detail_page.html",context)

