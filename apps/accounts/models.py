from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    patronymic = models.CharField("Отчество", max_length=150, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_full_name() or self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    bio = models.TextField("О себе", blank=True)
    subscribed_categories = models.ManyToManyField(
        "articles.Category", blank=True, verbose_name="Подписки на категории"
    )
    bookmarked_articles = models.ManyToManyField(
        "articles.Article", blank=True, verbose_name="Статьи в закладках"
    )
    bookmarked_news = models.ManyToManyField(
        "core.News", blank=True, verbose_name="Новости в закладках"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user.username}"
