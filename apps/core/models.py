from django.db import models


class RobotLoaderConfig(models.Model):
    """Singleton: настройки светящегося глаза в анимации загрузки."""
    # Смещение кольца от проецированного центра модели в пикселях экрана
    eye_x = models.FloatField("Смещение X (пиксели, вправо +)", default=0.0)
    eye_y = models.FloatField("Смещение Y (пиксели, вверх +)", default=0.0)
    # Радиус кольца в пикселях
    eye_size = models.FloatField("Радиус кольца (пиксели)", default=25.0)
    # Множитель яркости градиента (0 = невидимо, 1 = нормально, 2 = максимум)
    eye_intensity = models.FloatField("Яркость свечения (0–2)", default=1.0)
    # При каком прогрессе поворота (0–1) глаз начинает загораться
    eye_start_t = models.FloatField("Начало свечения (прогресс 0–1)", default=0.72)

    class Meta:
        verbose_name = "Настройки глаза робота"
        verbose_name_plural = "Настройки глаза робота"

    def __str__(self):
        return "Настройки глаза робота"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


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
