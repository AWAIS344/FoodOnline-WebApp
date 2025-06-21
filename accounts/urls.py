from django.urls import path,include
from . import views
from .api.views import RegisterUserAPI

urlpatterns = [
    path("",views.MyAccount),
    path('registeruser/',views.RegisterUser,name="register"),
    path('api/register/', RegisterUserAPI.as_view(), name='user-register'),

    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),

    path('myaccount',views.MyAccount,name="myaccount"),
    path("vend_dashboard/", views.Vend_dashboard, name="vend_dashboard"),
    path("cust_dashboard/", views.Cust_dashboard, name="cust_dashboard"),

    path("activate/<uidb64>/<token>/",views.Activate,name="activate"),
    # path('dashboard/',views.dashboard, name="dashboard"),

    #FORGOT_PASSWORD
    path("forgot_password/",views.Forgot_Password,name="forgot_password"),
    path("reset_password_validate/<uidb64>/<token>",views.Reset_Password_Validate,name="reset_password_validate"),
    path("reset_password/",views.Reset_Password,name="reset_password"),
    
    path("vendor/",include("vendor.urls"))
]
