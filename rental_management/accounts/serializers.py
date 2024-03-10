import re

from rest_framework import serializers
from .models import User


from django.core.validators import MinLengthValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    mobile_no = serializers.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(
                10, message="Mobile number should be exactly 10 digits."
            ),
        ],
        error_messages={
            "max_length": "Mobile number should be exactly 10 digits.",
        },
    )

    class Meta:
        model = User
        fields = ["email", "name", "address", "password", "password2", "mobile_no"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        mobile_no = data.get("mobile_no")
        if password != password2:
            raise serializers.ValidationError(
                {"message": "Password and Confirm Password doesn't match."}
            )
        if not re.match(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            raise serializers.ValidationError(
                {
                    "message": "Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:"
                }
            )

        if len(mobile_no) != 10:
            raise serializers.ValidationError("Mobile no should be 10 digits:")

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
            raise serializers.ValidationError(
                {"message": "Your are not registered user"}
            )


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=5)

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return super().create(validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, style={"input_type": "email"})
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                {"message": "Password and Confirm Password doesn't match."}
            )
        if not re.match(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            raise serializers.ValidationError(
                {
                    "message": "Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:"
                }
            )
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return data


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
