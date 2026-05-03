from django.db import models


class RoadmapStage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название этапа")
    description = models.TextField(verbose_name="Описание")
    period = models.CharField(max_length=100, verbose_name="Период (например: Q1 2025)")
    is_completed = models.BooleanField(default=False, verbose_name="Завершён")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Этап дорожной карты"
        verbose_name_plural = "Этапы дорожной карты"
        ordering = ["order"]

    def __str__(self):
        return self.title


class UlstuTeam(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название команды")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Команда УлГТУ"
        verbose_name_plural = "Команды УлГТУ"
        ordering = ["order"]

    def __str__(self):
        return self.name


class UlstuMember(models.Model):
    team = models.ForeignKey(
        UlstuTeam, on_delete=models.CASCADE, related_name="members", verbose_name="Команда"
    )
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    role = models.CharField(max_length=255, verbose_name="Роль")
    bio = models.TextField(blank=True, verbose_name="О себе")
    photo = models.ImageField(upload_to="ulstu/members/", blank=True, verbose_name="Фото")
    email = models.EmailField(blank=True, verbose_name="Email")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Участник проекта УлГТУ"
        verbose_name_plural = "Участники проекта УлГТУ"
        ordering = ["order"]

    def __str__(self):
        return self.full_name


class PrivacyPolicy(models.Model):
    content = models.TextField(verbose_name="Текст политики конфиденциальности")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

    def __str__(self):
        return f"Политика конфиденциальности (обновлена {self.updated_at.strftime('%d.%m.%Y')})"


class Application(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    specialty = models.CharField(max_length=255, verbose_name="Специальность / направление")
    motivation = models.TextField(verbose_name="Мотивация")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    is_processed = models.BooleanField(default=False, verbose_name="Обработана")

    class Meta:
        verbose_name = "Заявка на вступление"
        verbose_name_plural = "Заявки на вступление"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at.strftime('%d.%m.%Y')}"
