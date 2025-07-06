from django.urls import path
from . import views
from .api.views import VendorRegisterAPI
from accounts import views as AccountViews

urlpatterns = [
    path("registervendor/",views.RegisterVendor,name="registervendor"),
    path("api/register/", VendorRegisterAPI.as_view(), name="vendor-register"),

    path("",AccountViews.Vend_dashboard,name="vendor"),
    path("profile/",views.Vendor_Profile,name="vendor-profile"),
    path("menu-builder/",views.Menu_Builder,name="menu-builder"),
    path("menu-builder/catagory/<int:pk>",views.Food_Item_By_Catagory,name="food_item_by_catagory"),
    path("menu-builder/catagory/add",views.Add_Catagory,name="add_catagory"),
    path("menu-builder/catagory/edit<int:pk>",views.Edit_Catagory,name="edit_catagory"),


]
