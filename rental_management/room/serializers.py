from rest_framework import serializers
from .models import Room, Amenities, RoomImage


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ["ac", "free_wifi", "free_cable"]


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ["room", "image"]


class RoomSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer()
    images = RoomImageSerializer(many=True)

    class Meta:
        model = Room
        fields = [
            "user",
            "category",
            "title",
            "description",
            "price",
            "location",
            "is_available",
            "amenities",
            "images",
        ]


class RoomAddSerializer(serializers.ModelSerializer):

    amenities = AmenitiesSerializer(required=True)
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Room
        fields = [
            "user",
            "category",
            "title",
            "description",
            "price",
            "location",
            "is_available",
            "amenities",
            "images",
        ]

    def validate_images(self, value):
        if len(value) > 4:
            raise serializers.ValidationError("You can only upload up to 4 images.")
        return value

    def create(self, validated_data):
        amenities_data = validated_data.pop("amenities")
        images_data = validated_data.pop("images")

        room = Room.objects.create(**validated_data)

        if amenities_data:
            Amenities.objects.create(room=room, **amenities_data)

        if images_data:
            print("Image s herer")
            for image_data in images_data:
                RoomImage.objects.create(room=room, image=image_data)
        else:
            print("Image is not here ")
        return room
