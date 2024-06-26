from django.urls import path
from .views import (
    UserRegistrationView,
    ActivateAccountView,
    UserLoginView,
    GenerateOTPView,
    VerifyOTPView,
    ResetPasswordView,
    ChangePasswordView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate_account",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("forgot-password/", GenerateOTPView.as_view(), name="forgot-password"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
