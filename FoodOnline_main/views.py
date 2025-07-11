from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from menu.models import Catagory
from vendor.views import get_vendor

def Home(request):
    vendor=Vendor.objects.filter(is_approved=True,user__is_active=True)[:8].prefetch_related('categories')[:8]
    
    context={
        "vendor":vendor,
        
    }
    return render(request,"home.html",context)