from django.shortcuts import render,get_object_or_404,HttpResponse
from vendor.models  import Vendor
from menu.models import Catagory,FoodItems
from django.db.models import Prefetch
from django.http import JsonResponse
from .context_processors import get_cart_counter
from .models import Cart

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

    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'cart_items':cart_items,
        "vendor":vendor,
        "catagory":catagory,
    }
    return render(request,"detail_page.html",context)


def Add_to_Cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item=FoodItems.objects.get(id=food_id)

                try:
                    chkCart=Cart.objects.get(user=request.user, fooditem=food_item)
                    chkCart.quantity +=1
                    chkCart.save()
                    return JsonResponse({"status":"success","message":"Quantity Updated" ,"cart_counter":get_cart_counter(request)})

                except:
                    chkCart=Cart.objects.create(user=request.user, fooditem=food_item, quantity=1)
                    return JsonResponse({"status":"success","message":"Added to Cart","cart_counter":get_cart_counter(request)})


            except:
                return JsonResponse({"status":"failed","message":"This Food Doesnt Exit"})
        else:
            return JsonResponse({"status":"failed","message":"Invalid Request"})

        
    else:
        return JsonResponse({"status":"failed","message":"Please Login First"})
