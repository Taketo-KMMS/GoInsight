from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import AdminGroup, AdminUser


@admin.register(AdminUser)
class AdministratorAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "権限",
            {
                "fields": ("is_active", "is_superuser", "groups"),
            },
        ),
    )  # type: ignore
    list_display = ("username", "is_active", "is_superuser", "last_login")
    list_filter = ("is_superuser", "is_active", "groups")
    search_fields = ("username",)
    ordering = ("-created_at",)
    filter_horizontal = ("groups",)


admin.site.unregister(Group)
admin.site.register(AdminGroup)
