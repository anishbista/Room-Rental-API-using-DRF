from django.urls import path
from .views import *

urlpatterns = [
    path("", UserProfileView.as_view(), name="user-detail"),
]
