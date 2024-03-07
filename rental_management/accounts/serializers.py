import re
from django.forms import ValidationError
from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "password2", "mobile_no"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match."
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
