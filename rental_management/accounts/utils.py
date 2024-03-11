from django.core.mail import EmailMessage
import os
from django.contrib.sites.shortcuts import get_current_site


class Util:
    @staticmethod
    def send_email(email, otp):
        email = EmailMessage(
            subject="Forgot Password OTP",
            body=f"Your OTP is {otp}.",
            from_email=os.environ.get("EMAIL_FROM"),
            to=[email],
        )
        print(os.environ.get("EMAIL_FROM"))
        email.send()

    @staticmethod
    def send_verification_email(email, verification_link):
        email = EmailMessage(
            subject="Activate your account",
            body=verification_link,
            from_email=os.environ.get("EMAIL_FROM"),
            to=[email],
        )
        print(os.environ.get("EMAIL_FROM"))
        email.send()
