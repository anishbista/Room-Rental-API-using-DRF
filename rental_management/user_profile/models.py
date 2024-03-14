from django.db import models
from common.models import CommonInfo
from django.conf import settings
from room.models import Room


class Enquiry(CommonInfo):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_email = models.EmailField(
        verbose_name="email",
        max_length=255,
    )
    name = models.CharField(max_length=250)
    mobile_no = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"Room:{self.room}  customer={self.customer_email}"
