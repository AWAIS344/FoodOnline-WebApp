from django.contrib import admin
from .models import FoodItems,Catagory

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("catagory_name",)}
    list_display=['catagory_name',"vendor","updated_at",]
    search_fields=['catagory_name',"vendor__vendor_name"]


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("title",)}
    list_display=['title',"vendor", "price", "is_available","updated_at",]
    search_fields=['catagory__catagory_name',"vendor__vendor_name"]

# Register your models here.
admin.site.register(FoodItems,FoodItemAdmin)
admin.site.register(Catagory,CategoryAdmin)
