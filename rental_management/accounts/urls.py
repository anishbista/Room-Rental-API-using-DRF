from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("forgot-password/", GenerateOTPView.as_view(), name="forgot-password"),
    path("verify-password/", VerifyOTPView.as_view(), name="verify-password"),
]
