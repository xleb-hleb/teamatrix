from django.db import models


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, blank=True, default="bi-box", verbose_name="Bootstrap-иконка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = "Категории оборудования"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Material(models.Model):
    category = models.ForeignKey(
        EquipmentCategory, on_delete=models.CASCADE, related_name="materials", verbose_name="Категория"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    properties = models.TextField(blank=True, verbose_name="Характеристики")
    image = models.ImageField(upload_to="equipment/materials/", blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    url = models.URLField(blank=True, verbose_name="Сайт")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    categories = models.ManyToManyField(
        EquipmentCategory, blank=True, related_name="suppliers", verbose_name="Категории"
    )
    image = models.ImageField(upload_to="equipment/suppliers/", blank=True, verbose_name="Логотип")

    class Meta:
        verbose_name = "Поставщик / Фабрика"
        verbose_name_plural = "Поставщики / Фабрики"

    def __str__(self):
        return self.name
