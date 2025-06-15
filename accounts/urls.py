from django.urls import path
from . import views
from .api.views import RegisterUserAPI

urlpatterns = [
    path('registeruser/',views.RegisterUser,name="register"),
    path('api/register/', RegisterUserAPI.as_view(), name='user-register'),

    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),

    path('myaccount',views.MyAccount,name="myaccount"),
    path("vend_dashboard/", views.Vend_dashboard, name="vend_dashboard"),
    path("cust_dashboard/", views.Cust_dashboard, name="cust_dashboard"),

    path("activate/<uidb64>/<token>",views.Activate,name="activate")
    # path('dashboard/',views.dashboard, name="dashboard"),

]
