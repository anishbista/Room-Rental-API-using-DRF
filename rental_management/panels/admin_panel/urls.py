from django.urls import path
from panels.admin_panel.pages.user import UserListView, UserUpdateView

urlpatterns = [
    path("users/", UserListView.as_view(), name="admin_users"),
    path("users/<str:pk>/", UserUpdateView.as_view(), name="admin_users_update"),
]
