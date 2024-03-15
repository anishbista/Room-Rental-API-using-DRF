from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination


class RoomListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomAddView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request, format=None):
    #     # amenities_fields = (
    #     #     Amenities._meta.fields
    #     # )  # _meta.fields provides fields available in model

    #     # fields_name = [
    #     #     f"'{field.name}':'amenities.{field.name}" for field in amenities_fields
    #     # ][4:]

    #     # amenities_data = [
    #     #     {"name": "AC", "key": "amenities.ac"},
    #     #     {"name": "Wifi", "key": "amenities.free_wifi"},
    #     #     {"name": "Cable", "key": "amenities.Free_cable"},
    #     # ]
    #     return Response({"amenities": amenities_data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print(request.user.email)
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
