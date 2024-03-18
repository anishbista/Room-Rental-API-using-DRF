from django.urls import path
from .views import *

urlpatterns = [
    path("list/", RoomListView.as_view(), name="listRoom"),
    path("recently_added/", RecentlyAdded.as_view(), name="recentlyAdded"),
    path("add/", RoomAddView.as_view(), name="addRoom"),
    path("delete/<uuid:room_id>", RoomDeleteView.as_view(), name="deleteRoom"),
    path("<uuid:room_id>/", RoomDetailView.as_view(), name="detailRoom"),
    path("update/<uuid:room_id>/", RoomUpdateView.as_view(), name="updateRoom"),
]
