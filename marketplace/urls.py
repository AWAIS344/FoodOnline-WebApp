from django.urls import path
from . import views


urlpatterns = [
    path("",views.Marketplace,name='marketplace'),
    path("<slug:vendor_slug>",views.Detail_Page,name='detail_page'),

    #CART
    path("add_to_cart/<int:food_id>",views.Add_to_Cart,name='detail_page')



]