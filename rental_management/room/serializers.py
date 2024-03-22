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

    # amenities = AmenitiesSerializer(many=True)
    # images = RoomImageSerializer(many=True)
    amenities = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
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

    def get_amenities(self, obj):
        return [amenity.item for amenity in obj.amenities.all()]

    def get_images(self, obj):
        request = self.context.get("request")
        images_data = []
        for image in obj.images.all():
            image_data = {
                "url": request.build_absolute_uri(image.image.url),
                "id": image.id,
            }
            images_data.append(image_data)
        return images_data

    # request.build_absolute_uri => Returns the absolute URI form of location. If the location is already an absolute URI, it will not be altered. Otherwise the absolute URI is built using the server variables available in this request.


class RoomDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name")
    # amenities = AmenitiesSerializer(many=True)
    # images = RoomImageSerializer(many=True)
    amenities = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
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

    def get_amenities(self, obj):
        return [amenity.item for amenity in obj.amenities.all()]

    def get_images(self, obj):
        request = self.context.get("request")
        images_data = []
        for image in obj.images.all():
            image_data = {
                "url": request.build_absolute_uri(image.image.url),
                "id": image.id,
            }
            images_data.append(image_data)
        return images_data


class RoomAddSerializer(serializers.ModelSerializer):

    amenities = serializers.ListField(child=serializers.CharField(), required=False)
    images = serializers.ListField(child=serializers.ImageField(), required=True)

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

    def validate_image(self, value):
        print(f"sdadsadasdassd {len(value)}")
        if len(value) > 4 or len(value) < 2:
            raise serializers.ValidationError(
                {"message": "Minimum 2 and Maximum 4 images should be uploaded!"}
            )
        for image_data in value:
            if image_data.size > 1048576:
                raise serializers.ValidationError(
                    {"message": "The maximum file size that can be uploaded is 1 MB"}
                )
            if not image_data.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise serializers.ValidationError(
                    {
                        "message": "Only JPEG, JPG, or PNG images are allowed to be uploaded."
                    }
                )

        return value

    def create(self, validated_data):
        amenities_data = validated_data.pop("amenities", [])
        images_data = validated_data.pop("images")

        # if amenities_data:
        #     Amenities.objects.create(room=room, **amenities_data)
        result = self.validate_image(images_data)
        if result:
            room = Room.objects.create(**validated_data)
        if amenities_data:
            for item in amenities_data:
                Amenities.objects.create(room=room, item=item)

        if images_data:
            print("Image s herer")
            for image_data in images_data:
                RoomImage.objects.create(room=room, image=image_data)
        else:
            print("Image is not here ")
        return room


class RoomUpdateSerializer(serializers.ModelSerializer):

    amenities = serializers.ListField(child=serializers.CharField(), required=False)
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    removed_images = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    class Meta:
        model = Room
        fields = [
            "title",
            "description",
            "price",
            "location",
            "city",
            "amenities",
            "images",
            "is_available",
            "removed_images",
        ]

        # def validate_imagess(self, value):

        #     existing_images_count = self.instance.images.count() if self.instance else 0
        #     removed_images_count = len(self.initial_data.get("removed_images", []))

        #     print(f"removed_images       {removed_images_count}")

        #     total_images_count = existing_images_count + len(value) - removed_images_count

        # if total_images_count < 2:
        #     raise serializers.ValidationError(
        #         {"message": "At least 2 images should be provided"}
        #     )
        # elif total_images_count > 4:
        #     raise serializers.ValidationError(
        #         {"message": "Total number of images cannot exceed 4."}
        #     )

    #     # if len(value) > 4 or len(value) < 2:
    #     #     raise serializers.ValidationError(
    #     #         {"message": "Minimum 2 and Maximum 4 images should be uploaded!"}
    #     #     )
    #     for image_data in value:
    #         if image_data.size > 1048576:
    #             raise serializers.ValidationError(
    #                 {"message": "The maximum file size that can be uploaded is 1 MB"}
    #             )
    #         if not image_data.name.lower().endswith((".jpg", ".jpeg", ".png")):
    #             raise serializers.ValidationError(
    #                 {
    #                     "message": "Only JPEG, JPG, or PNG images are allowed to be uploaded."
    #                 }
    #             )

    #     return value
    def validate_image(self, value):
        # if len(value) > 4 or len(value) < 2:
        #     raise serializers.ValidationError(
        #         {"message": "Minimum 2 and Maximum 4 images should be uploaded!"}
        #     )
        for image_data in value:
            if image_data.size > 1048576:
                raise serializers.ValidationError(
                    {"message": "The maximum file size that can be uploaded is 1 MB"}
                )
            if not image_data.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise serializers.ValidationError(
                    {
                        "message": "Only JPEG, JPG, or PNG images are allowed to be uploaded."
                    }
                )

        return value

    def update(self, instance, validated_data):
        removed_images = validated_data.pop("removed_images", [])
        images_data = validated_data.pop("images")
        result = None
        if images_data:
            result = self.validate_image(images_data)

        print(f"Length of result     {len(result)}")

        print(f"dsadadad    {removed_images}")
        if result:
            for room_id in removed_images:
                try:
                    image_to_delete = RoomImage.objects.get(id=room_id)
                    image_to_delete.delete()
                except RoomImage.DoesNotExist:
                    pass

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.location = validated_data.get("location", instance.location)
        instance.city = validated_data.get("city", instance.city)
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )

        amenities_data = validated_data.get("amenities", [])
        images_data = validated_data.get("images", [])

        if amenities_data:
            instance.amenities.all().delete()
            for item in amenities_data:
                Amenities.objects.create(room=instance, item=item)

        if result:
            existing_images_count = self.instance.images.count() if self.instance else 0
            total_images_count = existing_images_count + len(result)
            if total_images_count < 2:
                raise serializers.ValidationError(
                    {"message": "At least 2 images should be provided"}
                )
            elif total_images_count > 4:
                raise serializers.ValidationError(
                    {"message": "Total number of images cannot exceed 4."}
                )
            for image_data in result:
                RoomImage.objects.create(room=instance, image=image_data)

        instance.save()
        return instance
