from django.core.mail import EmailMessage, EmailMultiAlternatives
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

    # @staticmethod
    # def send_verification_email(email, verification_link):
    #     email = EmailMessage(
    #         subject="Activate your account",
    #         body=verification_link,
    #         from_email=os.environ.get("EMAIL_FROM"),
    #         to=[email],
    #     )
    #     print(os.environ.get("EMAIL_FROM"))
    #     email.send()

    @staticmethod
    def send_verification_email(email, verification_link):
        msg = EmailMultiAlternatives(
            "Activate your account",
            verification_link,
            os.environ.get("EMAIL_FROM"),
            [email],
        )
        email = EmailMessage(
            subject="Activate your account",
            body=verification_link,
            from_email=os.environ.get("EMAIL_FROM"),
            to=[email],
        )
        print(os.environ.get("EMAIL_FROM"))
        email.send()


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
