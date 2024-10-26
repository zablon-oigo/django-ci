from django.urls import path

from .views import resend_otp_view, sign_in, sign_out, sign_up, verify_otp_view

urlpatterns = [
    path("register/", sign_up, name="register"),
    path("login/", sign_in, name="login"),
    path("verify/", verify_otp_view, name="verify"),
    path("logout/", sign_out, name="logout"),
    path("resend-otp/", resend_otp_view, name="resend_otp"),
]
