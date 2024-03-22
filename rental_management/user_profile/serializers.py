from rest_framework import serializers
from accounts.models import User
from .models import Enquiry
from room.models import Room


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "mobile_no", "address", "profile_picture"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "mobile_no", "address", "profile_picture"]
        extra_kwargs = {
            "name": {"required": False},
            "mobile_no": {"required": False},
            "address": {"required": False},
            "profile_picture": {"required": False},
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        mobile_no = data.get("mobile_no")
        profile_picture = data.get("profile_picture")
        if mobile_no and len(mobile_no) != 10:
            raise serializers.ValidationError(
                {"message": "Mobile number should be 10 digits"}
            )
        if profile_picture.size > 1048576:
            raise serializers.ValidationError(
                {"message": "The maximum file size that can be uploaded is 1 MB"}
            )

        return super().is_valid(raise_exception=raise_exception)


class EnquirySerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(write_only=True)
    room_name = serializers.CharField(source="room.title", read_only=True)

    class Meta:
        model = Enquiry
        fields = [
            "room_name",
            "room",
            "customer_email",
            "name",
            "mobile_no",
            "message",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        mobile_no = data.get("mobile_no")
        if mobile_no and len(mobile_no) != 10:
            raise serializers.ValidationError(
                {"message": "Mobile number should be 10 digits"}
            )
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, data):
        room_id = self.context["id"]
        user = self.context["user"]

        room_user = Room.objects.filter(id=room_id).first()
        print(f"room  {room_user.user.email}        user: {user.email}")

        if room_user.user.email == user.email:
            raise serializers.ValidationError(
                {"message": "Enquiring own room not allowed!"}
            )
        return data

    def create(self, validated_data):
        return Enquiry.objects.create(**validated_data)


# class UserEnquirySerializer(serializers.ModelSerializer):
#     room = serializers.CharField(source="room.title")
#     room_id = serializers.CharField()

#     class Meta:
#         model = Enquiry
#         fields = [
#             "room_id",
#             "room",
#             "name",
#             "mobile_no",
#             "message",
#         ]
