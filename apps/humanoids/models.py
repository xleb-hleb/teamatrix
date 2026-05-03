from django.db import models


class HumanoidPost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    summary = models.TextField(verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to="humanoids/posts/", blank=True, verbose_name="Изображение")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статья о гуманоидах"
        verbose_name_plural = "Статьи о гуманоидах"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class HumanoidVideo(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    youtube_url = models.URLField(verbose_name="Ссылка на YouTube")
    thumbnail = models.ImageField(upload_to="humanoids/videos/", blank=True, verbose_name="Превью")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_embed_url(self):
        """Конвертирует YouTube URL в embed-ссылку."""
        import re
        patterns = [
            r"(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return f"https://www.youtube.com/embed/{match.group(1)}"
        return self.youtube_url
