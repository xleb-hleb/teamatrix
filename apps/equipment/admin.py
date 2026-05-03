from django.contrib import admin

from .models import EquipmentCategory, Material, Supplier


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MaterialInline]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    filter_horizontal = ("categories",)
    search_fields = ("name", "country")
