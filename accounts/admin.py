from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    AdminUserCreationForm,
    UserChangeForm,
)
from django.utils.translation import gettext_lazy as _


# Register your models here.

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = AdminUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "email", "first_name", "last_name", "is_staff", 'is_student', 'is_academic_personal','is_searcher',)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups",'is_student', 'is_academic_personal','is_searcher')
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","bio","profile_photo","phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_student",
                    "is_academic_personal",
                    'is_searcher'
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )



admin.site.register(User, UserAdmin)
