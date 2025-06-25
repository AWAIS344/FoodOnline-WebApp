from .models import User,UserProfile
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
    
    def clean(self):
        cleaned_data=super(UserRegForm,self).clean()
        password=cleaned_data.get("password")

        confirm_password=cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
            "Both The Password Should Match")
        

class UserProfileForm(forms.ModelForm):
    profile_image=forms.ImageField(widget=forms.FileInput(attrs={"class":"btn btn-info"}))
    cover_image=forms.ImageField(widget=forms.FileInput(attrs={"class":"btn btn-info"}))
    class Meta:
        model = UserProfile
        exclude = ["user", "created_at", "modified_at"]


    