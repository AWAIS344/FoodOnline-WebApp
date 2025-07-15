from .models import  Cart
from menu.models import FoodItems

def get_cart_counter(request):
    cart_count=0

    if request.user.is_authenticated:
        try:
            cart_item=Cart.objects.filter(user=request.user)
            
            for item in cart_item:
                cart_count+=item.quantity
        except:
            cart_count=0
    return dict(cart_count=cart_count)