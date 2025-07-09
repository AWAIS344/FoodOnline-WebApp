from django import forms
from .models import Catagory,FoodItems
from vendor.validator import allow_only_image_validator

class CatagoryForm(forms.ModelForm):

    class Meta:
        model = Catagory
        fields=['catagory_name','description']


class FoodItemsForm(forms.ModelForm):
    image=forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}),validators=[allow_only_image_validator])
    class Meta:
        model = FoodItems
        fields=["catagory",'title','price',"image","is_available","description" ,"image"]