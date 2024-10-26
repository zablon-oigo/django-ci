from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

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


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=100, min_length=6, widget=forms.PasswordInput, label="Password"
    )
    confirm_password = forms.CharField(
        max_length=100,
        min_length=6,
        widget=forms.PasswordInput,
        label="Confirm Password",
    )
    uidb64 = forms.CharField(widget=forms.HiddenInput)
    token = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        uidb64 = cleaned_data.get("uidb64")
        token = cleaned_data.get("token")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("The reset link is invalid or has expired")
            user.set_password(password)
            user.save()

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError("The reset link is invalid or has expired")

        return cleaned_data
