from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination
from .permissions import IsRoomOwner
import uuid


def get_object(room_id):
    return get_object_or_404(Room, id=room_id)


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

    # def get_permissions(self):
    #     if self.request.method in ["DELETE", "PUT"]:
    #         return [IsAuthenticated()]
    #     return []

    def get(self, request, room_id, format=None):
        room = self.get_object(room_id)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsRoomOwner]

    def delete(self, request, room_id, format=None):
        room = get_object(room_id)
        room.delete()
        return Response(
            {"message": "Room deleted successfully!"}, status=status.HTTP_204_NO_CONTENT
        )


class RoomUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsRoomOwner]

    def put(self, request, room_id, format=None):
        try:
            room = get_object(room_id)
        except:
            return Response(
                {"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        print(f"Accessing user:{request.user}")
        print(f"owner:{room.user}")

        print(request.user == room.user)

        data = request.data.copy()
        data.pop("images", None)
        print(f"imagesssssssssssS:{data}")

        serializer = RoomAddSerializer(room, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Room updated successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if request.user == room.user:
        #     serializer = RoomAddSerializer(room, data=request.data, partial=True)

        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(
        #             {"message": "Room updated successfully"},
        #             status=status.HTTP_201_CREATED,
        #         )
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(
        #     {"message": "You are not authorized to update"},
        #     status=status.HTTP_401_UNAUTHORIZED,
        # )
