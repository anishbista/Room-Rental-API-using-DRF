from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

    # def send_email(email_data):
    #     api_url = os.environ.get("API_URl")
    #     print(os.environ.get("AUTHORIZATION_KEY"))
    #     print(f"{api_url}dsadadasadssda")
    #     headers = {
    #         "Authorization": os.environ.get("AUTHORIZATION_KEY"),
    #         "Content-Type": "application/json",
    #     }
    #     data = {
    #         "subject": email_data["subject"],
    #         "message": email_data["message"],
    #         "sender_email": os.environ.get("EMAIL_FROM"),
    #         "receiver_email": email_data["receiver_email"],
    #         "smtp_server": "smtp.gmail.com",
    #         "smtp_port": 587,
    #         "smtp_username": os.environ.get("EMAIL_USER"),
    #         "smtp_password": os.environ.get("EMAIL_PASS"),
    #     }

    #     response = requests.post(url=api_url, json=data, headers=headers)

    #     if response.status_code == 200:
    #         print("Email sent successfully")
    #     else:
    #         print("Failed to send email")
    # def send_email(email_data):

    #     message_html = render_to_string(
    #         "send_mail.html",
    #         {
    #             "subject": email_data["subject"],
    #             "message": email_data["message"],
    #         },
    #     )
    #     # print(f"Message:  {message}")
    #     # print(f"type of message is {type(message)}")
    #     plain_message = strip_tags(message_html)
    #     print(f"plain message : {plain_message}")
    #     print("Type of plain message")
    #     print(type(plain_message))
    #     email = EmailMultiAlternatives(
    #         email_data["subject"],
    #         plain_message,
    #         os.environ.get("EMAIL_FROM"),
    #         [email_data["receiver_email"]],
    #     )
    #     email.attach_alternative(message_html, "text/html")
    #     email.send()

    def send_email(email_data):

        email_html_message = render_to_string(
            "send_mail.html",
            {
                "subject": email_data["subject"],
                "message": email_data["message"],
                "type": email_data["type"],
            },
        )
        plain_message = strip_tags(email_html_message)
        msg = EmailMultiAlternatives(
            email_data["subject"],
            plain_message,
            os.environ.get("EMAIL_FROM"),
            [email_data["receiver_email"]],
        )

        msg.attach_alternative(email_html_message, "text/html")
        sent = msg.send(fail_silently=False)
        # data = {
        #     "subject": email_data["subject"],
        #     "message": email_data["message"],
        #     "sender_email": os.environ.get("EMAIL_FROM"),
        #     "receiver_email": email_data["receiver_email"],
        #     "smtp_server": "smtp.gmail.com",
        #     "smtp_port": 587,
        #     "smtp_username": os.environ.get("EMAIL_USER"),
        #     "smtp_password": os.environ.get("EMAIL_PASS"),
        # }

        # response = requests.post(url=api_url, json=data, headers=headers)

        # if response.status_code == 200:
        #     print("Email sent successfully")
        # else:
        #     print("Failed to send email")

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
