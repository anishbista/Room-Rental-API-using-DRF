from django.urls import path
from .views import *

urlpatterns = [
    path("", UserProfileView.as_view(), name="user-detail"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("room/", UserRoomView.as_view(), name="user-detail"),
    path("enquiry/", EnquiryView.as_view(), name="enquiry"),
    path("enquiryList/", UserEnquiryView.as_view(), name="enquiryList"),
]
