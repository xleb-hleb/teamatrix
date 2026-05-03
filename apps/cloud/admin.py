import mimetypes

from django.contrib import admin
from django.utils.html import format_html

from .models import CloudFile


@admin.register(CloudFile)
class CloudFileAdmin(admin.ModelAdmin):
    list_display = (
        "original_name",
        "size_human",
        "mime_type",
        "description_short",
        "uploaded_at",
        "download_button",
    )
    list_display_links = ("original_name",)
    readonly_fields = (
        "original_name",
        "size",
        "size_human",
        "mime_type",
        "uploaded_at",
        "download_link_field",
    )
    fields = (
        "file",
        "description",
        "original_name",
        "size_human",
        "mime_type",
        "uploaded_at",
        "download_link_field",
    )
    search_fields = ("original_name", "description", "mime_type")
    date_hierarchy = "uploaded_at"

    # ── Сохранение: извлекаем мета-данные из загружаемого файла ──

    def save_model(self, request, obj, form, change):
        if "file" in request.FILES:
            uploaded = request.FILES["file"]
            obj.original_name = uploaded.name
            obj.size = uploaded.size
            mime, _ = mimetypes.guess_type(uploaded.name)
            obj.mime_type = mime or "application/octet-stream"
        super().save_model(request, obj, form, change)

    # ── Колонка со ссылкой в списке ──

    @admin.display(description="Скачать")
    def download_button(self, obj):
        url = obj.get_download_url()
        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="padding:3px 10px;background:#417690;color:#fff;'
            'border-radius:4px;text-decoration:none;font-size:12px;">'
            '⬇ Скачать</a>',
            url,
        )

    # ── Поле «Прямая ссылка» в форме редактирования ──

    @admin.display(description="Прямая ссылка для скачивания")
    def download_link_field(self, obj):
        if not obj.pk:
            return "—"
        url = obj.get_download_url()
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
            '<code id="cloud-dl-url" style="background:#1a1a2e;color:#7dd3fc;'
            'padding:6px 12px;border-radius:4px;font-size:13px;word-break:break-all;">'
            '{}</code>'
            '<button type="button" onclick="'
            'navigator.clipboard.writeText(window.location.origin+\'{}\');'
            'this.textContent=\'✓ Скопировано\';setTimeout(()=>this.textContent=\'Копировать\',2000);" '
            'style="padding:5px 12px;background:#28a745;color:#fff;border:none;'
            'border-radius:4px;cursor:pointer;font-size:12px;white-space:nowrap;">'
            'Копировать</button>'
            '<a href="{}" target="_blank" '
            'style="padding:5px 12px;background:#417690;color:#fff;border-radius:4px;'
            'text-decoration:none;font-size:12px;white-space:nowrap;">'
            '⬇ Скачать</a>'
            '</div>',
            url, url, url,
        )

    # ── Вспомогательные методы ──

    @admin.display(description="Описание")
    def description_short(self, obj):
        return (obj.description[:60] + "…") if len(obj.description) > 60 else obj.description or "—"
