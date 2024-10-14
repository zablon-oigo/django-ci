import pyotp
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from .models import CustomUser


def send_code_to_user(request, email):
    user = CustomUser.objects.get(email=email)
    if not user.secret_key:
        user.secret_key = pyotp.random_base32()
    otp = pyotp.TOTP(user.secret_key, interval=300).now()
    request.session["user_email"] = email
    current_site = "example.com"
    subject = "Email Verification"
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f9fafb;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); padding: 20px;">
            <h2 style="color: #1f2937; font-size: 24px;">Dear {user.username},</h2>
            <p style="color: #4b5563; font-size: 16px;">Thank you for registering on <strong>{current_site}</strong></p>
            <p style="color: #4b5563; font-size: 16px;">To complete your registration and verify your email address, please use the following one-time passcode (OTP):</p>
            <h3 style="color: #007BFF; font-size: 20px; font-weight: bold; text-align: center; display: block;">{otp}</h3>
            <p style="color: #4b5563; font-size: 16px;">This code is valid for <strong>5 minutes</strong>. Please use it promptly. If you did not sign up for an account, please disregard this email.</p>
            <p style="color: #4b5563; font-size: 16px;">If you have any questions or need further assistance, feel free to contact our support team at <a href="mailto:support@example.com" style="color: #007BFF; text-decoration: underline;">support@example.com</a>.</p>
            <br>
            <p style="color: #4b5563; font-size: 16px;">Best regards,<br>The {current_site} Team</p>
        </div>
    </body>
    </html>
    """
    from_email = settings.EMAIL_HOST_USER
    send_email = EmailMessage(
        subject=subject, body=email_body, from_email=from_email, to=[email]
    )
    send_email.content_subtype = "html"
    send_email.send(fail_silently=False)
    user.otp_created_at = timezone.now()
    user.save()
