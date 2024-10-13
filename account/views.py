from datetime import timedelta

import pyotp
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import LoginForm, RegisterUser, VerifyForm
from .models import CustomUser
from .utils import send_code_to_user


def sign_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, "Login request was successfull")
                return redirect("list")
        messages.error(request, "Invalid username or password")
    form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()

            send_code_to_user(request, user.email)
            return redirect("verify")

    else:
        form = RegisterUser()

    return render(request, "accounts/register.html", {"form": form})


def sign_out(request):
    logout(request)
    messages.success(request, "Logout request was successfull")
    return redirect("login")


def verify_otp_view(request):
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            user_email = request.session.get("user_email")
            user = CustomUser.objects.get(email=user_email)

            otp_expiry_time = user.otp_created_at + timedelta(minutes=300)
            if timezone.now() > otp_expiry_time:
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect("resend_otp")
            otp_instance = pyotp.TOTP(user.secret_key, interval=300)
            user_otp = form.cleaned_data["otp"]
            if otp_instance.verify(user_otp, valid_window=1):
                messages.success(request, "OTP verified successfully!")
                return redirect("blog:list")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
    else:
        form = VerifyForm()

    return render(request, "accounts/verify.html", {"form": form})


def resend_otp_view(request):
    user_email = request.session.get("user_email")
    user = CustomUser.objects.get(email=user_email)
    send_code_to_user(request, user.email)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect("verify")
