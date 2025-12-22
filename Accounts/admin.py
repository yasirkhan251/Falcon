from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, LoginOTP, Forgotpassword


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    """
    Admin configuration for custom user model
    Login via PHONE
    """

    model = MyUser

    # Columns shown in user list
    list_display = (
        "server_id",
        "phone",
        "name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_filter = ("is_active", "is_staff", "is_superuser")

    search_fields = ("phone", "name", "server_id")

    ordering = ("-date_joined",)

    # Fields shown while viewing/editing a user
    fieldsets = (
        (None, {
            "fields": ("phone", "password")
        }),
        ("Personal Info", {
            "fields": ("name", "profile", "server_id", "doj")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser")
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    # Fields shown while ADDING a user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "name", "password1", "password2"),
        }),
    )

    readonly_fields = ("server_id", "date_joined", "last_login")

    # Since login is via phone
    def get_username(self, obj):
        return obj.phone


@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "otp", "created_at")
    search_fields = ("phone",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Forgotpassword)
class ForgotpasswordAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "expires_at")
    search_fields = ("user__phone",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
