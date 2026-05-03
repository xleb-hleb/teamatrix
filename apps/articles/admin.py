from django.contrib import admin

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "is_published", "views_count", "created_at"]
    list_filter = ["is_published", "category", "created_at"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published"]
