import mimetypes
import os
import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse

cloud_storage = FileSystemStorage(
    location=settings.BASE_DIR / "static" / "cloud",
    base_url="/static/cloud/",
)


def _cloud_upload_path(instance, filename):
    """Сохраняем с UUID-именем, чтобы избежать коллизий."""
    ext = os.path.splitext(filename)[1].lower()
    return f"{uuid.uuid4().hex}{ext}"


class CloudFile(models.Model):
    original_name = models.CharField(max_length=255, verbose_name="Имя файла")
    file = models.FileField(
        upload_to=_cloud_upload_path,
        storage=cloud_storage,
        verbose_name="Файл",
    )
    size = models.BigIntegerField(default=0, verbose_name="Размер (байт)")
    mime_type = models.CharField(max_length=100, blank=True, verbose_name="MIME-тип")
    description = models.TextField(blank=True, verbose_name="Описание")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.original_name

    def get_download_url(self):
        return reverse("cloud:download", kwargs={"pk": self.pk})

    def size_human(self):
        size = self.size
        for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
            if size < 1024:
                return f"{size:.1f}\u00a0{unit}"
            size /= 1024
        return f"{size:.1f}\u00a0ТБ"

    size_human.short_description = "Размер"
