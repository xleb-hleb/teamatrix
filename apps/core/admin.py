from django.contrib import admin

from .models import News, TeamMember


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published"]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["full_name", "position", "order"]
    list_editable = ["order"]
    search_fields = ["full_name", "position"]

