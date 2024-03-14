from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
import jwt


class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomAddView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        amenities_fields = (
            Amenities._meta.fields
        )  # _meta.fields provides fields available in model

        fields_name = [field.name for field in amenities_fields][4:]

        return Response({"amenities": fields_name}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print(request.user.email)
        serializer = RoomAddSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Room added successfully!"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
