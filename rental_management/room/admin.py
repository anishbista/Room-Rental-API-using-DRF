from django.contrib import admin
from .models import Room, RoomImage, Amenities


class RoomImageStackedInLine(admin.StackedInline):
    model = RoomImage
    max_num = 4


class AmenitiesStackedInLine(admin.StackedInline):
    model = Amenities


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "category", "price", "is_available"]
    date_hierarchy = "created_on"
    inlines = [AmenitiesStackedInLine, RoomImageStackedInLine]
