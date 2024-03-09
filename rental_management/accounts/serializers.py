import re
from django.forms import ValidationError
from rest_framework import serializers
from .models import User
import random
from accounts.utils import Util


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
                {"Password": "Password and Confirm Password doesn't match."}
            )
        if not re.match(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            raise serializers.ValidationError(
                "Password must minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:"
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
        if User.objects.filter(email=email).first():
            user = User.objects.get(email=email)
            otp = random.randint(1000, 9999)
            data = {
                "subject": "Forgot Password OTP",
                "body": f"Your OTP is {otp}.",
                "to_email": user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError({"Email": "Your are not registered user"})
