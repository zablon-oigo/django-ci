from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser
from django import forms
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=("email",)

class RegisterUser(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['email','password1','password2']

    def clean_password(self):
        cd=self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password did not match')
        return cd['password2']
    def clean_email(self):
        data=self.cleaned_data['email']
        qs=CustomUser.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email is already in use !!!!")
        return data
class LoginForm(forms.Form):
    email=forms.CharField(max_length=65)
    password=forms.CharField(max_length=65)