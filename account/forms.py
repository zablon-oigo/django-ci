from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class RegisterUser(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def clean_password(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Password did not match")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = CustomUser.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email is already in use!")
        return data


class LoginForm(forms.Form):
    email = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65)


class VerifyForm(forms.Form):
    otp = forms.CharField(
        label="Enter OTP",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your OTP",
                "class": "",
            }
        ),
        error_messages={
            "required": "Please enter the OTP.",
            "max_length": "OTP must be exactly 6 digits long.",
            "min_length": "OTP must be exactly 6 digits long.",
        },
    )

    def clean_otp(self):
        otp = self.cleaned_data.get("otp")
        if not otp.isdigit():
            raise forms.ValidationError("OTP must be numeric.")
        return otp


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No user is associated with this email address."
            )
        return email
