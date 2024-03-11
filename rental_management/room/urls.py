from django.urls import path
from .views import *

urlpatterns = [
    path("list/", RoomListView.as_view(), name="listRoom"),
    path("add/", RoomAddView.as_view(), name="addRoom"),
]
