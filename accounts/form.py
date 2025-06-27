from .models import User,UserProfile
from  django import forms
from vendor.validator import allow_only_image_validator

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
    profile_image=forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}),validators=[allow_only_image_validator])
    cover_image=forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}),validators=[allow_only_image_validator])
    class Meta:
        model = UserProfile
        exclude = ["user", "created_at", "modified_at"]


    #MAKING THE FIELDS READONLY
    def _init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "latitude" or field == "longitude":
                self.fields['field'].widget.attrs['readonly']='readonly'


    