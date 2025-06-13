from .models import Vendor
from  django import forms


class VendorRegForm(forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields=["vendor_name","vendor_license"]
