from django.contrib import admin
from .models import *


@admin.register(Enquiry)
class Enquiry(admin.ModelAdmin):
    list_display = ["room_title", "customer_email", "name", "mobile_no"]

    def room_title(self, obj):
        return obj.room.title

    room_title.short_description = "Room"
