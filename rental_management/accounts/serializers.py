import re

from rest_framework import serializers
from .models import User


from django.core.validators import MinLengthValidator


def password_validation(password, password2):
    if password != password2:
        raise serializers.ValidationError(
            {"message": "Password and Confirm Password doesn't match"}
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
    return password


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "address",
            # "profile_picture",
            "password",
            "password2",
            "mobile_no",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "address": {"required": True},
            "mobile_no": {"required": True},
            "email": {"required": True},
            "name": {"required": True},
            "password2": {"required": True},
            # "profile_picture": {"required": True},
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        mobile_no = data.get("mobile_no")
        password = data.get("password")
        password2 = data.get("password2")
        # profile_picture = data.get("profile_picture")

        email = data.get("email")
        registered_user = User.objects.filter(email=email).first()
        if registered_user:
            raise serializers.ValidationError(
                {
                    "message": "User with this email already exists but haven't verified your email."
                }
            )

        if mobile_no and len(mobile_no) != 10:
            raise serializers.ValidationError(
                {"message": "Mobile number should be 10 digits"}
            )
        # if profile_picture.size > 1048576:
        #     raise serializers.ValidationError(
        #         {"message": "The maximum file size that can be uploaded is 1 MB"}
        #     )

        if password is None or password2 is None:
            raise serializers.ValidationError(
                {"message": "Password or Confirm Password is missing."}
            )
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
        return super().is_valid(raise_exception=raise_exception)

    # def validate(self, data):
    #     password = data.get("password")
    #     password2 = data.get("password2")

    #     if password != password2:
    #         raise serializers.ValidationError(
    #             {"message": "Password and Confirm Password doesn't match."}
    #         )
    #     if not re.match(
    #         "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    #         password,
    #     ):
    #         raise serializers.ValidationError(
    #             {
    #                 "message": "Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:"
    #             }
    #         )

    #     return data

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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)

    def validate(self, data):
        user = self.context["user"]
        print(f"User:           {user}")
        old_password = data.get("old_password")
        print(f"old_password:           {old_password}")
        password = data.get("password")
        print(f"password:           {password}")
        password2 = data.get("password2")
        print(f"password2:           {user.check_password(old_password)}")
        if not user.check_password(old_password):
            raise serializers.ValidationError({"message": "Old password is incorrect."})
        valid_password = password_validation(password, password2)
        if valid_password:
            user.set_password(valid_password)
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
