from .models import User
from  django import forms

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Enter Password','class':"foodbakery-dev-req-field"
}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Re-Enter Your Password'
}))
    
    class Meta:
        model=User
        fields=["first_name","last_name","username","password","phone_number","email"]