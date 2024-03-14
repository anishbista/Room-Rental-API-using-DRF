from django.contrib import admin
from .models import Room, RoomImage


class RoomImageStackedInLine(admin.StackedInline):
    model = RoomImage
    max_num = 4


# class AmenitiesStackedInLine(admin.StackedInline):
#     model = Amenities
#     max_num = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "category", "price"]
    date_hierarchy = "created_on"
    inlines = [RoomImageStackedInLine]
