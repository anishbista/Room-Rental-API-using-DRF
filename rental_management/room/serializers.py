from rest_framework import serializers
from .models import Room, RoomImage, Amenities


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = [
            "item",
        ]


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ["room", "image"]


class RoomSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True)
    images = RoomImageSerializer(many=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "user",
            "category",
            "title",
            "description",
            "price",
            "city",
            "location",
            "is_available",
            "amenities",
            "images",
        ]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Customizing the response as needed
    #     custom_data = {
    #         "roomId": data["id"],
    #         "user": data["user"],
    #         "category": data["category"],
    #         "title": data["title"],
    #         "description": data["description"],
    #         "price": float(data["price"]),  # Converting DecimalField to float
    #         "location": data["location"],
    #         "available": data["is_available"],
    #         "images": [img["image"] for img in data["images"]],  # Extracting image URLs
    #     }
    #     return custom_data


class RoomAddSerializer(serializers.ModelSerializer):

    amenities = serializers.ListField(child=serializers.CharField(), required=False)
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
            "city",
            "amenities",
            "images",
        ]

    def validate_images(self, value):
        print(f"sdadsadasdassd {len(value)}")
        if len(value) > 4 or len(value) < 2:
            raise serializers.ValidationError(
                "Minimum 2 and Maximum 4 images should be uploaded!"
            )
        return value

    def create(self, validated_data):
        amenities_data = validated_data.pop("amenities", [])
        images_data = validated_data.pop("images")

        room = Room.objects.create(**validated_data)

        # if amenities_data:
        #     Amenities.objects.create(room=room, **amenities_data)
        if amenities_data:
            for item in amenities_data:
                Amenities.objects.create(room=room, item=item)

        if images_data:
            print("Image s herer")
            for image_data in images_data:
                if image_data.size > 1048576:
                    raise serializers.ValidationError(
                        {
                            "message": "The maximum file size that can be uploaded is 1 MB"
                        }
                    )
                RoomImage.objects.create(room=room, image=image_data)
        else:
            print("Image is not here ")
        return room
