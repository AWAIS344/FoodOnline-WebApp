from .models import Vendor
from  django import forms


class VendorRegForm(forms.ModelForm):
    vendor_license=forms.ImageField(widget=forms.FileInput(attrs={"class":"btn btn-info"}))
    class Meta:
        model = Vendor
        fields=["vendor_name","vendor_license"]
