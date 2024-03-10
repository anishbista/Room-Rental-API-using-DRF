import random
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .renders import UserRenderer
from .models import User
from .utils import Util
from .models import OTP


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(
        user,
    )
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "message": "Registration Successful."},
                status=status.HTTP_201_CREATED,
            )
        errors = serializer.errors.copy()
        print(errors)
        # error_messages = []
        # for field_errors in errors.values():
        #     if isinstance(field_errors, list):
        #         for error in field_errors:
        #             error_messages.append(str(error))
        #     else:
        #         error_messages.append(str(field_errors))
        # print(error_messages)
        # del errors["non_field_errors"]
        # print(errors)
        # print("ErrorDetail" in str(errors))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            print(f"user:{type(user)}")
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "message": "Login Successful."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Email or Password is not valid",
                },
                status=status.HTTP_404_NOT_FOUND,
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
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            otp = str(random.randint(1000, 9999))
            OTP.objects.create(user=user, otp=otp)
            Util.send_email(email, otp)
            return Response(
                {"message": "Otp sent. Please check your email"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class VerifyOTPView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]
            print(f"coming otp:{otp}")
            # print(f"otp:{request.session['reset_password_otp']}")

            if (
                "reset_password_otp" in request.session
                and "reset_password_email" in request.session
            ):
                if (
                    request.session["reset_password_otp"] == otp
                    and request.session["reset_password_email"] == email
                ):
                    del request.session["reset_password_otp"]
                    del request.session["reset_password_email"]
                    return Response(
                        {"message": "OTP verified successfully."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Invalid OTP or email."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Session data not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
