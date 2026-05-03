from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Описание")
    location = models.CharField(max_length=255, blank=True, verbose_name="Место проведения")
    date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    url = models.URLField(blank=True, verbose_name="Ссылка на мероприятие")
    image = models.ImageField(upload_to="events/", blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ["date"]

    def __str__(self):
        return self.title
