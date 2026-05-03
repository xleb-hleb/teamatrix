from django.db import models


class News(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("URL-адрес", unique=True)
    summary = models.TextField("Краткое описание")
    content = models.TextField("Содержание")
    image = models.ImageField("Изображение", upload_to="news/", blank=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=255)
    bio = models.TextField("Биография", blank=True)
    photo = models.ImageField("Фото", upload_to="team/")
    email = models.EmailField("Email", blank=True)
    order = models.PositiveIntegerField("Порядок отображения", default=0)

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Наша команда"
        ordering = ["order"]

    def __str__(self):
        return self.full_name
