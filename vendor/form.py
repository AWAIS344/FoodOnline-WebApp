from .models import Vendor
from  django import forms
from .validator import allow_only_image_validator


class VendorRegForm(forms.ModelForm):
    vendor_license=forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}),validators=[allow_only_image_validator])
    class Meta:
        model = Vendor
        fields=["vendor_name","vendor_license"]
