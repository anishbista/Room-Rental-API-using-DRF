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

# from rest_framework.decorators import extend_schema,extend_schema_view


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# @extend_schema_view(
#     post=extend_schema(
#         tags=["Enquiry"
#               ]
#     )
# )


class UserRoomView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        print(f"user: {user.id}")
        return Room.objects.filter(user=user)


class EnquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.data["customer_email"] = request.user.email
        serializer = EnquirySerializer(data=request.data)

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
