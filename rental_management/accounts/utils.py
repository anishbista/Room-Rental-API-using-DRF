from django.core.mail import EmailMessage, EmailMultiAlternatives
import requests
import os
from django.contrib.sites.shortcuts import get_current_site


class Util:
    # @staticmethod  # staticmethod is that the method can be called without creating an instance of the class and doesn't require self parameter also
    # def send_email(email, otp):
    #     email = EmailMessage(
    #         subject="Forgot Password OTP",
    #         body=f"Your OTP is {otp}.",
    #         from_email=os.environ.get("EMAIL_FROM"),
    #         to=[email],
    #     )
    #     print(os.environ.get("EMAIL_FROM"))
    #     email.send()

    def send_email(email_data):
        api_url = os.environ.get("API_URl")
        print(os.environ.get("AUTHORIZATION_KEY"))
        print(f"{api_url}dsadadasadssda")
        headers = {
            "Authorization": os.environ.get("AUTHORIZATION_KEY"),
            "Content-Type": "application/json",
        }
        data = {
            "subject": email_data["subject"],
            "message": email_data["message"],
            "sender_email": os.environ.get("EMAIL_FROM"),
            "receiver_email": email_data["receiver_email"],
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_username": os.environ.get("EMAIL_USER"),
            "smtp_password": os.environ.get("EMAIL_PASS"),
        }

        response = requests.post(url=api_url, json=data, headers=headers)

        if response.status_code == 200:
            print("Email sent successfully")
        else:
            print("Failed to send email")

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

    # @staticmethod
    # def send_verification_email(email, verification_link):
    #     msg = EmailMultiAlternatives(
    #         "Activate your account",
    #         verification_link,
    #         os.environ.get("EMAIL_FROM"),
    #         [email],
    #     )
    #     email = EmailMessage(
    #         subject="Activate your account",
    #         body=verification_link,
    #         from_email=os.environ.get("EMAIL_FROM"),
    #         to=[email],
    #     )
    #     print(os.environ.get("EMAIL_FROM"))
    #     email.send()


# def send_mail_function(email,context):
#     msg = EmailMultiAlternatives(
#         str('Verif your email! - "') + "{title}".format(title='A2Z Marmat App'),
#         "Verfisy your email!",
#         os.environ.get("EMAIL_FROM"),
#         [email],
#     )
#     email_html_message = render_to_string("email/user_registration_confirm.html",context)

#     msg.attach_alternative(email_html_message,"text/html")
#     sent = msg.send(fail_silently=False)
