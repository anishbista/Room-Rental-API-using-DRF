from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    list_display = ["email", "name", "mobile_no", "is_admin", "profile_picture"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "mobile_no", "profile_picture"]}),
        (
            "Permissions",
            {
                "fields": ["is_admin"],
            },
        ),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "name",
                    "mobile_no",
                    "password1",
                    "password2",
                    "profile_picture",
                ],
            },
        ),
    ]
    search_fields = [
        "email",
    ]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserModelAdmin)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["user", "otp", "created_on"]
