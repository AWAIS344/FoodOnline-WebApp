from django import forms
from .models import Catagory,FoodItems

class CatagoryForm(forms.ModelForm):

    class Meta:
        model = Catagory
        fields=['catagory_name','description']


class FoodItemsForm(forms.ModelForm):

    class Meta:
        model = FoodItems
        fields=["catagory",'title','price',"image","is_available","description"]