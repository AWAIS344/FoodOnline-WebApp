from django.shortcuts import render
from vendor.models  import Vendor

# Create your views here.

def Marketplace(request):
    vendor=Vendor.objects.filter(is_approved=True,user__is_active=True)[:8].prefetch_related('categories')
    vendor_count=vendor.count()
    context={
        "vendor_count":vendor_count,
        "vendor":vendor
    }
    return render(request,"marketplace.html",context)