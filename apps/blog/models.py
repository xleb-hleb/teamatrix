from django.conf import settings
from django.db import models


class Thread(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_threads",
        verbose_name="Автор",
    )
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="forum_threads",
        verbose_name="Статья",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    views_count = models.PositiveIntegerField("Просмотры", default=0)
    is_pinned = models.BooleanField("Закреплено", default=False)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ["-is_pinned", "-updated_at"]

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Тема",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_posts",
        verbose_name="Автор",
    )
    content = models.TextField("Сообщение")
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="Ответ на",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]

    def __str__(self):
        return f"Сообщение от {self.author} в «{self.thread}»"