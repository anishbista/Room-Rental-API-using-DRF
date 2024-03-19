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
