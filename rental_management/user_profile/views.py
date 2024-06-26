from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import generics
from accounts.models import User
from .serializers import (
    UserProfileSerializer,
    UserUpdateSerializer,
    EnquirySerializer,
)
from .models import *
from accounts.utils import Util
from room.serializers import RoomSerializer
from common.pagination import CustomPagination
import threading
from drf_spectacular.utils import extend_schema, extend_schema_view

# from rest_framework.decorators import extend_schema,extend_schema_view


def send_email_in_thread(email_data):
    Util.send_enquiry(email_data)


@extend_schema_view(
    get=extend_schema(
        tags=["Profile"],
        summary="User Profile View API ",
        description="User Profile View API ",
    )
)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    put=extend_schema(
        tags=["Profile"],
        summary="User Profile Update API",
        description="User Profile Update API",
        request=UserUpdateSerializer,
    )
)
class UserUpdateView(APIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=self.get_object(), data=request.data, partial=True
        )
        profile_link = None
        if serializer.is_valid():
            serializer.save()
            profile_link = (
                request.build_absolute_uri(request.user.profile_picture.url)
                if request.user.profile_picture
                else None
            )
            return Response(
                {
                    "message": "Profile updated successfully",
                    "name": request.user.name,
                    "mobile_no": request.user.mobile_no,
                    "address": request.user.address,
                    "email": request.user.email,
                    "profile_picture": profile_link,
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserUpdateView(generics.UpdateAPIView):
#     serializer_class = UserUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user


@extend_schema_view(
    get=extend_schema(
        tags=["Profile"],
        summary="User Room List API ",
        description="User Room List API ",
    )
)
class UserRoomView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user).order_by("-created_on")


@extend_schema_view(
    get=extend_schema(
        tags=["Profile"],
        summary="User Enquiry List API ",
        description="User Enquiry List API ",
    )
)
class UserEnquiryView(generics.ListAPIView):
    serializer_class = EnquirySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Enquiry.objects.filter(customer_email=self.request.user.email).order_by(
            "-created_on"
        )


@extend_schema_view(
    post=extend_schema(
        tags=["Profile"],
        summary="User Enquiry API",
        description="User Enquiry API",
        request=EnquirySerializer,
        # responses={201: EnquirySerializer},
    )
)
class EnquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # print(f"Request tpe: {request.data._mutable}")
        # request.data._mutable = True
        # print(f"Before:   {request.data}")
        mutable_data = request.data.copy()

        mutable_data["customer_email"] = request.user.email
        # request.data._mutable = False
        print(f"After:   {request.data}")
        serializer = EnquirySerializer(
            data=mutable_data,
            context={"user": request.user, "id": request.data.get("room")},
        )

        # print(f"dadadadadadadada: {request.data.get('room')}")
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            room = serializer.validated_data["room"]
            roomname = Room.objects.get(id=request.data.get("room"))
            # print(f"roomname: {roomname.user.email}")
            # print(f"email: {roomname}")

            # print(f"validated data {serializer.validated_data}")
            print(f"Landlord email: {roomname.user.email}")

            print(f"customer email:{serializer.validated_data['customer_email']}")

            email_data = {
                "subject": f"Enquiry about {roomname.title}",
                "landlord_name": roomname.user.name,
                "room_title": roomname.title,
                "customer_name": serializer.validated_data["name"],
                "customer_email": serializer.validated_data["customer_email"],
                "customer_mobile": serializer.validated_data["mobile_no"],
                "message": serializer.validated_data["message"],
                "receiver_email": roomname.user.email,
            }

            email_thread = threading.Thread(
                target=send_email_in_thread, args=(email_data,), daemon=True
            )
            email_thread.start()

            # Util.send_enquiry(email_data)
            return Response(
                {"message": "Enquired Successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
