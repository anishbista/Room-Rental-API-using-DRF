from django.db import models
from common.models import CommonInfo, room_category
from django.conf import settings
from django.core.exceptions import ValidationError


class Room(CommonInfo):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=250)
    # category = models.CharField(choices=room_category, max_length=20)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    is_expired = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return str(self.id)


class RoomImage(CommonInfo):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room_images/")


class Amenities(CommonInfo):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="amenities")
    item = models.CharField(max_length=250)
