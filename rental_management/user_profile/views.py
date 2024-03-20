from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import generics
from accounts.models import User
from .serializers import *
from .models import *
from accounts.utils import Util
from room.serializers import RoomSerializer
from common.pagination import CustomPagination


# from rest_framework.decorators import extend_schema,extend_schema_view


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserRoomView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)


class UserEnquiryView(generics.ListAPIView):
    serializer_class = EnquirySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Enquiry.objects.filter(customer_email=self.request.user.email)


class EnquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # print(f"Request tpe: {request.data._mutable}")
        # request.data._mutable = True
        # print(f"Before:   {request.data}")
        request.data["customer_email"] = request.user.email
        # request.data._mutable = False
        print(f"After:   {request.data}")
        serializer = EnquirySerializer(
            data=request.data,
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

            Util.send_enquiry(email_data)
            return Response(
                {"message": "Enquired Successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
