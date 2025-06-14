from django.urls import path
from . import views
from .api.views import VendorRegisterAPI

urlpatterns = [
    path("registervendor/",views.RegisterVendor,name="registervendor"),
    path("api/register/", VendorRegisterAPI.as_view(), name="vendor-register"),
]
