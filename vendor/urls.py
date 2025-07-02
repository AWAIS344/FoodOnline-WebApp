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

]
