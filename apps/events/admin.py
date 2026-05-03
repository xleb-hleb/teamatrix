from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"
