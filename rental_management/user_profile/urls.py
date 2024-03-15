from django.urls import path
from .views import *

urlpatterns = [
    path("", UserProfileView.as_view(), name="user-detail"),
    path("enquiry/", EnquiryView.as_view(), name="enquiry"),
]
