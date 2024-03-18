from rest_framework import serializers
from .models import Room, RoomImage, Amenities
from accounts.models import User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name")
    """ 
    - The "user" field is customized using serializers.CharField(source='user.name').
    - source='user.name' means that it should get the value for the "user" field from the "name" attribute of the related User model.
    - serializers.CharField is used to directly represent the user's name as a string.
    """

    amenities = AmenitiesSerializer(many=True)
    images = RoomImageSerializer(many=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Room
        fields = [
            "created_on",
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


class RoomDetailSerializer(serializers.ModelSerializer):
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

    def update(self, room, validated_data):
        room.title = validated_data.get("title", room.title)
        room.description = validated_data.get("description", room.description)
        room.price = validated_data.get("price", room.price)
        room.location = validated_data.get("location", room.location)
        room.city = validated_data.get("city", room.city)

        amenities_data = validated_data.get("amenities", [])
        images_data = validated_data.get("images")

        if amenities_data:
            for item in amenities_data:
                Amenities.object.create(room=room, item=item)

        if images_data:
            for item in images_data:
                if item.size > 1048576:
                    raise serializers.ValidationError(
                        {
                            "message": "The maximum file size that can be uploaded is 1 MB"
                        }
                    )
                RoomImage.objects.create(room=room, image=item)

        room.save()
        return room
