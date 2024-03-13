from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = (
    [
        path(
            "admin/",
            include(
                [
                    path("", include("customadmin.urls")),
                    path("", include("panels.admin_panel.urls")),
                ]
            ),
        ),
        path("dj-admin/", admin.site.urls),
        path("api/profile/", include("user_profile.urls")),
        path("api/user/", include("accounts.urls")),
        path("api/room/", include("room.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
