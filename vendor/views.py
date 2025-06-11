from django.shortcuts import render

# Create your views here.
def RegisterVendor(request):
    
    context={}
    return render(request,"registervendor.html",context)