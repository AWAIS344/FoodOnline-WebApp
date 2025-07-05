from django import forms
from .models import Catagory

class CatagoryForm(forms.ModelForm):

    class Meta:
        model = Catagory
        fields=['catagory_name','description']