from django.contrib import admin
from .models import User, Profile, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "fullname", "phone", "is_admin"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["email", "fullname", "phone"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "nickname", "birthday", "is_public"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user", "nickname"]
    raw_id_fields = ["user"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["id", "user_from", "user_to"]
    list_filter = ["created_at"]
    search_fields = ["user_from", "user_to"]
    raw_id_fields = ["user_from", "user_to"]
