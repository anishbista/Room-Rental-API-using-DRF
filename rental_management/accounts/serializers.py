import re
from django.forms import ValidationError
from rest_framework import serializers
from .models import User
import random
from accounts.utils import Util
from django.contrib.sessions.models import Session


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "address", "password", "password2", "mobile_no"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                {"error": "Password and Confirm Password doesn't match."}
            )
        if not re.match(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            raise serializers.ValidationError(
                {
                    "error": "Password must minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:"
                }
            )

        return data

    def create(self, validate_data):

        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            return attrs
        else:
            raise serializers.ValidationError({"error": "Your are not registered user"})


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.IntegerField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255)

#     def validate(self, attrs):
#         email = attrs.get("email")
#         if User.objects.filter(email=email).first():
#             otp = random.randint(1000, 9999)
#             user = User.objects.get(email=email)
#             data = {
#                 "subject": "Forgot Password OTP",
#                 "body": f"Your OTP is {otp}.",
#                 "to_email": user.email,
#             }
#             Util.send_email(data)
#             return attrs
#         else:
#             raise serializers.ValidationError({"Email": "Your are not registered user"})
