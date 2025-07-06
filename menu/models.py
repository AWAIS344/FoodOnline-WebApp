from django.db import models
from vendor.models import Vendor


class Catagory(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    catagory_name=models.CharField(max_length=60,unique=True)
    slug=models.SlugField(unique=True,max_length=50)
    description=models.TextField(max_length=250,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='catagory'
        verbose_name_plural='catagories'
        
    def clean(self):
        self.catagory_name = self.catagory_name.capitalize()
    def __str__(self):
        return self.catagory_name


class FoodItems(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to="foodimages")
    is_available=models.BooleanField(default=True)
    slug=models.SlugField(unique=True,max_length=50)
    description=models.TextField(max_length=250,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


