from django.core.mail import EmailMessage
import os


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
