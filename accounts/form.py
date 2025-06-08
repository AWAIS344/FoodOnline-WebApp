from .models import User
from  django import forms

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Enter Password'
}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Re-Enter Your Password'
}))
    
    class Meta:
        model=User
        fields=["first_name","last_name","user_name","password",]