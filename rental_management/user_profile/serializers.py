from rest_framework import serializers
from accounts.models import User
from .models import Enquiry


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "mobile_no", "address", "profile_picture"]


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            "room",
            "customer_email",
            "name",
            "mobile_no",
            "message",
        ]

        def create(self, validated_data):
            Enquiry.objects.create(**validated_data)
