from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import (
    RoomUpdateSerializer,
    RoomSerializer,
    RoomDetailSerializer,
    RoomAddSerializer,
    Room,
)
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPagination
from .permissions import IsRoomOwner
import uuid
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, filters
from django_filters import FilterSet, RangeFilter

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


def get_object(room_id):
    return get_object_or_404(Room, id=room_id)


class RoomFilter(FilterSet):
    price = RangeFilter()

    class Meta:
        model = Room
        fields = ["price", "category", "location", "city", "is_available"]


@extend_schema_view(
    get=extend_schema(
        tags=["Rooms"],
        summary="Rooms List API ",
        description="User List API ",
    )
)
class RoomListView(ListAPIView):
    pagination_class = CustomPagination
    # queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    # filterset_fields = ["city", "category"]
    filterset_class = RoomFilter
    ordering = ["-created_on"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        return Room.objects.all().order_by("-created_on")


""" Customized filter query
 """
# class RoomListView(APIView):
#     pagination_class = CustomPagination

#     def get(self, request):
#         queryset = Room.objects.all()
#         title = request.query_params.get("search")
#         price_max = request.query_params.get("price_max")
#         price_min = request.query_params.get("price_min")
#         if title is not None:
#             print(f"title: {title}")
#             queryset = Room.objects.filter(title__icontains=title)
#             print(queryset)

#         if price_min is not None:
#             queryset = Room.objects.filter(price__gte=price_min)
#         if price_max is not None:
#             queryset = Room.objects.filter(price__lte=price_max)

#         paginator = self.pagination_class()
#         result_page = paginator.paginate_queryset(queryset, request)
#         serializer = RoomSerializer(
#             result_page, many=True, context={"request": request}
#         )
#         return paginator.get_paginated_response(serializer.data)


@extend_schema_view(
    post=extend_schema(
        tags=["Rooms"],
        summary="Room Create API",
        description="Room Create API",
        request=RoomAddSerializer,
        responses=[
            OpenApiResponse(examples=[{}]),
        ],
    ),
)
class RoomAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print(f"Request data:  {request.data}")
        # for x, y in request.data.items():
        #     print(f"{x}    {y}")
        # mutable_data = request.data.copy()
        mutable_data = request.data

        mutable_data["user"] = request.user.id
        # request.data["user"] = request.user.id
        serializer = RoomAddSerializer(data=mutable_data)

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


@extend_schema_view(
    get=extend_schema(
        tags=["Rooms"],
        summary="Rooms Detail API ",
        description="User Detail API ",
    )
)
class RoomDetailView(APIView):
    serializer_class = RoomDetailSerializer

    def get(self, request, room_id, format=None):
        room = get_object(room_id)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        tags=["Rooms"],
        summary="Room Delete API",
        description="Room Delete API",
        responses=[
            OpenApiResponse(examples=[{}]),
        ],
    ),
)
class RoomDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsRoomOwner]

    def delete(self, request, room_id, format=None):
        room = get_object(room_id)
        room.delete()
        return Response(
            {"message": "Room deleted successfully!"}, status=status.HTTP_204_NO_CONTENT
        )


@extend_schema_view(
    put=extend_schema(
        tags=["Rooms"],
        summary="Room Update API",
        description="Room Update API",
        request=RoomUpdateSerializer,
        responses=[
            OpenApiResponse(examples=[{}]),
        ],
    ),
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

        print(f"imagesssssssssssS:{request.data}")

        serializer = RoomUpdateSerializer(room, data=request.data, partial=True)
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


@extend_schema_view(
    get=extend_schema(
        tags=["Rooms"],
        summary="Recently Added API ",
        description="Recently Added API ",
    )
)
class RecentlyAdded(ListAPIView):
    pagination_class = CustomPagination
    before_two_days = timezone.now() - timedelta(days=2)
    print(f"before:    {before_two_days}")
    queryset = Room.objects.filter(created_on__gte=before_two_days).order_by(
        "-created_on"
    )

    serializer_class = RoomSerializer
