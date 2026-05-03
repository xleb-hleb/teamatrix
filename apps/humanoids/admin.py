from django.contrib import admin

from .models import HumanoidPost, HumanoidVideo


@admin.register(HumanoidPost)
class HumanoidPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"


@admin.register(HumanoidVideo)
class HumanoidVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title",)
