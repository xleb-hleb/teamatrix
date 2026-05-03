from django.contrib import admin

from .models import Post, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "article", "is_pinned", "views_count", "created_at"]
    list_filter = ["is_pinned", "created_at"]
    list_editable = ["is_pinned"]
    search_fields = ["title", "author__username"]
    raw_id_fields = ["article"]
    date_hierarchy = "created_at"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "thread", "is_deleted", "created_at"]
    list_filter = ["is_deleted", "created_at"]
    list_editable = ["is_deleted"]
    search_fields = ["author__username", "content"]
    raw_id_fields = ["thread", "reply_to"]