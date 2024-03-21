import random
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User, OTP
from .utils import Util
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
import threading


def send_email_in_thread(email_data):
    Util.send_email(email_data)


def get_tokens_for_user(request, user):
    refresh = RefreshToken.for_user(
        user,
    )
    current_site = get_current_site(request)
    print(f"current_site: sadsadasd {current_site}")

    profile_link = (
        f"http://{current_site}/{user.profile_picture.url}"
        if user.profile_picture
        else None
    )

    token_payload = {
        "email": user.email,
        "name": user.name,
        "mobile_no": user.mobile_no,
        "profile_pic": profile_link,
    }
    # access_token = str(refresh.access_token)
    refresh.payload.update(token_payload)

    return {
        "access": str(refresh.access_token),
    }


@extend_schema_view(
    post=extend_schema(
        tags=["Registration"],
        description="Account registration API -description",
        summary="Account registration API -summary",
    )
)
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            print(f"User after serializing {user}")
            user.is_active = False
            user.save()
            email = serializer.validated_data.get("email")
            verification_link = self.generate_verification_link(request, user)
            email_message = f"Please click <a href='{verification_link}'>this link</a> to activate your account."
            email_data = {
                "subject": "Activate your account",
                "message": verification_link,
                "receiver_email": email,
                "type": "registration",
            }
            email_thread = threading.Thread(
                target=send_email_in_thread,
                args=(email_data,),
                daemon=True,
            )
            email_thread.start()
            # Util.send_email(email_data)
            return Response(
                {
                    "message": "Link has been sent to your email. Click the link to verify."
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_verification_link(self, request, user):
        current_site = get_current_site(request)
        print(
            f"current_site - {current_site}             current_site_domain - {current_site.domain}"
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return f"http://{current_site.domain}/api/user/activate/{uid}/{token}/"


class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        print("Im in activated")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse(
                "Account activated successfully", status=status.HTTP_200_OK
            )
        else:
            # Handle invalid token or user not found
            return HttpResponse(
                "Invalid activation link", status=status.HTTP_400_BAD_REQUEST
            )


# class OTPVerificationView(APIView):
#     def post(self, request, format=None):
#         email = request.data.get("email")
#         otp_entered = request.data.get("otp")
#         # Get unverified OTP record
#         unverified_otp = get_object_or_404(UnverifiedOTP, email=email)
#         if unverified_otp.otp == otp_entered:
#             # OTP verified successfully, proceed with user registration
#             serializer = UserRegistrationSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 user = serializer.save()
#                 return Response(
#                     {"message": "Registered successfully."},
#                     status=status.HTTP_201_CREATED,
#                 )
#         return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


# class UserRegistrationView(APIView):

#     def post(self, request, format=None):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.validated_data.get("email")
#             print(f"serialized validated data: {email}")
#             user = serializer.save()
#             token = get_tokens_for_user(user)
#             return Response(
#                 {"token": token, "message": "Registered Successful."},
#                 status=status.HTTP_201_CREATED,
#             )
#         errors = serializer.errors.copy()
#         print(errors)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyRegisterEmailView(APIView):
#     def post(self, request, format=None):
#         email = request.data.get("email")
#         otp = str(random.randint(1000, 9999))
#         UnverifiedOTP.create(email=email, otp=otp)
#         Util.send_email(email, otp)
#         return Response({"message": "Otp sent"})


class UserLoginView(APIView):
    # renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")

        registered_user = User.objects.filter(email=email).first()

        print(f"Check:  {request.is_secure()}")
        if registered_user:
            if registered_user.is_active:
                user = authenticate(email=email, password=password)
                if user:
                    print(f"user:{type(user)}")
                    token = get_tokens_for_user(request, user)
                    current_site = get_current_site(request)
                    if request.is_secure():
                        profile_link = (
                            f"https://{current_site}/{user.profile_picture.url}"
                            if user.profile_picture
                            else None
                        )
                    else:
                        profile_link = (
                            # f"http://{current_site}/{user.profile_picture.url}"
                            request.build_absolute_uri(user.profile_picture.url)
                            if user.profile_picture
                            else None
                        )
                    return Response(
                        {
                            "name": user.name,
                            "mobile_no": user.mobile_no,
                            "address": user.address,
                            "email": user.email,
                            "profile_picture": profile_link,
                            "token": token,
                            "message": "Login Successfully.",
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Invalid Credentials!!"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return Response(
                    {
                        "message": "You haven't verified your email. Click the link sent to your mail to verify and again try"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"message": "Invalid Credentials!!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # email = request.data.get("email")
        # user = User.objects.filter(email=email).first()
        # if user:
        #     otp = random.randint(1000, 9999)

        #     send_mail(
        #         "Forgot Password OTP",
        #         f"Your OTP is {otp}.",
        #         "anishbista9237@gmail.com",
        #         [user.email],
        #         fail_silently=False,
        #     )
        #     request.session["forgot_password_otp"] = otp
        #     request.session["forgot_password_email"] = email
        #     return Response(
        #         {"message": "OTP sent Successfully."}, status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(
        #         {"error": "User with this email does not exist."},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )


# Code of GenerateOTPView before
# def post(self, request, format=None):


#     serializer = ForgotPasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data["email"]
#         user = User.objects.get(email=email)
#         otp = random.randint(1000, 9999)
#         Util.send_email(email, otp)
#         request.session["reset_password_otp"] = otp
#         request.session["reset_password_email"] = email
#         return Response(
#             {"msg": "Otp sent. Please check your email"},
#             status=status.HTTP_200_OK,
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GenerateOTPView(APIView):
    # renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            if user.is_active:
                otp = str(random.randint(1000, 9999))
                already_otp = OTP.objects.filter(user=user).first()
                if already_otp:
                    OTP.objects.filter(user=user).delete()

                OTP.objects.create(user=user, otp=otp)
                email_data = {
                    "subject": "Forgot Password OTP",
                    "message": otp,
                    "receiver_email": email,
                    "type": "otp",
                }

                # email_thread = threading.Thread(
                #     target=send_email_in_thread, args=(email_data,)
                # )
                # email_thread.start()
                Util.send_email(email_data)
                return Response(
                    {
                        "message": "Otp sent. Please check your email",
                        "email": f"{email}",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "You haven't verified your email. Click the link sent to your mail to verify and again try"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # def delete_expired_otps(self):
    #     expired_time = timezone.now() + timedelta(minutes=1)
    #     OTP.objects.filter(created_on__lt=expired_time).delete()


class VerifyOTPView(APIView):
    def post(self, request, format=None):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")

        otp_obj = OTP.objects.filter(user__email=email, otp=otp).first()
        if otp_obj:
            otp_obj.delete()
            return Response(
                {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetPasswordView(APIView):
    # renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user and user.is_active:
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid():

                return Response(
                    {"message": "Password Changed successfully"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"message": "You haven't been registered!!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyOTPView(APIView):
#     renderer_classes = [UserRenderer]

#     def post(self, request, format=None):
#         serializer = VerifyOTPSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             otp = serializer.validated_data["otp"]
#             print(f"coming otp:{otp}")
#             # print(f"otp:{request.session['reset_password_otp']}")

#             if (
#                 "reset_password_otp" in request.session
#                 and "reset_password_email" in request.session
#             ):
#                 if (
#                     request.session["reset_password_otp"] == otp
#                     and request.session["reset_password_email"] == email
#                 ):
#                     del request.session["reset_password_otp"]
#                     del request.session["reset_password_email"]
#                     return Response(
#                         {"message": "OTP verified successfully."},
#                         status=status.HTTP_200_OK,
#                     )
#                 else:
#                     return Response(
#                         {"message": "Invalid OTP or email."},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             else:
#                 return Response(
#                     {"message": "Session data not found."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            return Response(
                {"message": "Password Changed Successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
