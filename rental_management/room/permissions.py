from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Room


class IsRoomOwner(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     print(f"dsadadadadadada:{obj.user == request.user}")
    #     return obj.user == request.user
    message = "You are not the owner of this room or do not have permission to perform this action."

    def has_permission(self, request, view):
        room_id = view.kwargs.get("room_id")
        try:
            room = get_object_or_404(Room, id=room_id)
        except Room.DoesNotExist:
            return False
        return request.user == room.user
