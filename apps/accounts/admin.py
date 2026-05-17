from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    filter_horizontal = ("bookmarked_articles", "bookmarked_news", "subscribed_categories")
    fieldsets = (
        ("Профиль", {"fields": ("avatar", "bio")}),
        ("Закладки", {"fields": ("bookmarked_articles", "bookmarked_news")}),
        ("Подписки", {"fields": ("subscribed_categories",)}),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
