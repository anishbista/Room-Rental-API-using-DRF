from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination
import uuid


class RoomListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.data["user"] = request.user.id
        serializer = RoomAddSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            print(f"Added room data: {serializer.validated_data}")
            return Response(
                {
                    "message": "Room added successfully!",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):
    serializer_class = RoomDetailSerializer

    def get_permissions(self):
        if self.request.method in ["DELETE", "PUT"]:
            return [IsAuthenticated()]
        return []

    def get_object(self, room_id):
        return get_object_or_404(Room, id=room_id)

    def get(self, request, room_id, format=None):
        room = self.get_object(room_id)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_id, format=None):
        room = self.get_object(room_id)
        room.delete()
        return Response(
            {"message": "Room deleted successfully!"}, status=status.HTTP_204_NO_CONTENT
        )
