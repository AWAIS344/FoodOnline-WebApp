from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def RegisterUser(request):
    return HttpResponse("This is User Registration")