from django.db import models
from common.models import CommonInfo, room_category
from django.conf import settings
from django.core.exceptions import ValidationError


class Room(CommonInfo):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(choices=room_category, max_length=20)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=250)
    is_expired = models.BooleanField(default=False)
    is_available = models.BooleanField()

    def __str__(self):
        return f"Title: {self.title}   User:{self.user}"


class RoomImage(CommonInfo):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room_images/")


class Amenities(CommonInfo):
    room = models.OneToOneField(
        Room, on_delete=models.CASCADE, related_name="amenities"
    )
    ac = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    free_cable = models.BooleanField(default=False)
