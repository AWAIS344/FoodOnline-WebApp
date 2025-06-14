from django.urls import path
from . import views
from .api.views import RegisterUserAPI

urlpatterns = [
    path('registeruser/',views.RegisterUser,name="register"),
    path('api/register/', RegisterUserAPI.as_view(), name='user-register'),

    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),
    path('dashboard/',views.dashboard, name="dashboard"),

]
