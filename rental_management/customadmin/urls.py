from django.urls import path
from .views import admin_login, dashboard

urlpatterns = [
    path("", admin_login, name="admin_login"),
    path("dashboard/", dashboard, name="dashboard"),
]
