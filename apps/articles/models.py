from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL-адрес", unique=True)
    description = models.TextField("Описание", blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_breadcrumbs(self):
        breadcrumbs = []
        category = self
        while category:
            breadcrumbs.insert(0, category)
            category = category.parent
        return breadcrumbs


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("URL-адрес", unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория", related_name="articles"
    )
    summary = models.TextField("Аннотация")
    content = CKEditor5Field("Содержание", config_name="default")
    image = models.ImageField("Изображение", upload_to="articles/", blank=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    views_count = models.PositiveIntegerField("Просмотры", default=0)
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
