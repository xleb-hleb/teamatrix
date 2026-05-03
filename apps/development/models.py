from django.db import models
from django.urls import reverse


class Subsystem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="development/subsystems/", blank=True, verbose_name="Изображение")
    icon = models.CharField(max_length=50, blank=True, default="bi-cpu", verbose_name="Bootstrap-иконка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Подсистема"
        verbose_name_plural = "Подсистемы"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Component(models.Model):
    subsystem = models.ForeignKey(
        Subsystem, on_delete=models.CASCADE, related_name="components", verbose_name="Подсистема"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    specs = models.TextField(blank=True, verbose_name="Характеристики")
    purpose = models.TextField(verbose_name="Назначение")
    buy_url = models.URLField(blank=True, verbose_name="Ссылка для заказа")
    image = models.ImageField(upload_to="development/components/", blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Комплектующее"
        verbose_name_plural = "Комплектующие"

    def __str__(self):
        return self.name


class ReadySolution(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    url = models.URLField(blank=True, verbose_name="Ссылка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Готовое решение"
        verbose_name_plural = "Готовые решения"
        ordering = ["order"]

    def __str__(self):
        return self.name


class DevSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Содержание")
    icon = models.CharField(max_length=50, blank=True, default="bi-tools", verbose_name="Bootstrap-иконка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Раздел разработки"
        verbose_name_plural = "Разделы разработки"
        ordering = ["order"]

    def __str__(self):
        return self.title


class RobotBodyPart(models.Model):
    PART_CHOICES = [
        ('head', 'Голова'),
        ('torso', 'Туловище'),
        ('left_arm', 'Левая рука'),
        ('right_arm', 'Правая рука'),
        ('pelvis', 'Таз'),
        ('left_leg', 'Левая нога'),
        ('right_leg', 'Правая нога'),
    ]

    key = models.CharField(
        max_length=30,
        choices=PART_CHOICES,
        unique=True,
        verbose_name="Идентификатор части тела",
    )
    label = models.CharField(max_length=100, verbose_name="Название")
    color = models.CharField(
        max_length=30,
        blank=True,
        default="",
        verbose_name="Цвет (CSS)",
        help_text="Например: #00d4ff или rgba(0,212,255,0.8)",
    )
    progress = models.PositiveIntegerField(
        default=0,
        verbose_name="Прогресс разработки (%)",
        help_text="Целое число от 0 до 100",
    )
    subsystem = models.ForeignKey(
        Subsystem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="body_parts",
        verbose_name="Связанная подсистема",
    )
    description = models.TextField(blank=True, verbose_name="Описание (для всплывающего окна)")
    controllers = models.TextField(
        blank=True,
        verbose_name="Контроллеры и электроника",
        help_text="Описание CAN-шины, моторных контроллеров, бортового ПК и т.д.",
    )

    class Meta:
        verbose_name = "Часть тела робота"
        verbose_name_plural = "Части тела робота"
        ordering = ['key']

    def __str__(self):
        return f"{self.label} ({self.progress}%)"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.progress > 100:
            raise ValidationError({'progress': 'Прогресс не может превышать 100%'})

    def get_url(self):
        return reverse('development:robot_part_detail', kwargs={'key': self.key})


class RobotElectronics(models.Model):
    body_part = models.ForeignKey(
        RobotBodyPart,
        on_delete=models.CASCADE,
        related_name="electronics",
        verbose_name="Часть тела",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    name = models.CharField(max_length=100, verbose_name="Название")
    purpose = models.CharField(max_length=255, verbose_name="Назначение")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Электроника / контроллер"
        verbose_name_plural = "Электроника и контроллеры"
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} — {self.purpose}"


class RobotBOMItem(models.Model):
    body_part = models.ForeignKey(
        RobotBodyPart,
        on_delete=models.CASCADE,
        related_name="bom_items",
        verbose_name="Часть тела",
    )
    name = models.CharField(max_length=255, verbose_name="Наименование")
    quantity = models.CharField(max_length=50, verbose_name="Количество", help_text="Например: 5, по BOM, набор")
    acquisition = models.CharField(
        max_length=50,
        verbose_name="Способ получения",
        help_text="Например: Купить, Печать, Сборка",
    )
    material = models.CharField(max_length=100, blank=True, verbose_name="Материал/тип")
    note = models.TextField(blank=True, verbose_name="Примечание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "BOM-позиция"
        verbose_name_plural = "BOM-позиции"
        ordering = ["order"]

    def __str__(self):
        return self.name


class RobotDrawing(models.Model):
    body_part = models.ForeignKey(
        RobotBodyPart,
        on_delete=models.CASCADE,
        related_name="drawings",
        verbose_name="Часть тела",
    )
    label = models.CharField(max_length=255, verbose_name="Подпись")
    url = models.URLField(verbose_name="Ссылка на CAD / файл")
    source = models.CharField(max_length=100, blank=True, verbose_name="Источник", help_text="Например: Onshape, MakerWorld")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "CAD-чертёж / модель"
        verbose_name_plural = "CAD-чертежи / модели"
        ordering = ["order"]

    def __str__(self):
        return self.label


class RobotReference(models.Model):
    body_part = models.ForeignKey(
        RobotBodyPart,
        on_delete=models.CASCADE,
        related_name="references",
        verbose_name="Часть тела",
    )
    label = models.CharField(max_length=255, verbose_name="Подпись")
    url = models.URLField(verbose_name="Ссылка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Справочная ссылка"
        verbose_name_plural = "Справочные ссылки"
        ordering = ["order"]

    def __str__(self):
        return self.label


class RobotAssemblyStep(models.Model):
    body_part = models.ForeignKey(
        RobotBodyPart,
        on_delete=models.CASCADE,
        related_name="assembly_steps",
        verbose_name="Часть тела",
    )
    title = models.CharField(max_length=255, verbose_name="Название шага")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Этап сборки"
        verbose_name_plural = "Этапы сборки"
        ordering = ["order"]

    def __str__(self):
        return self.title


class GitHubLink(models.Model):
    TYPE_MODELS = "models"
    TYPE_SOFTWARE = "software"
    TYPE_CHOICES = [
        (TYPE_MODELS, "3D-модели"),
        (TYPE_SOFTWARE, "Программные решения"),
    ]
    title = models.CharField(max_length=255, verbose_name="Название")
    url = models.URLField(verbose_name="Ссылка на GitHub")
    description = models.TextField(blank=True, verbose_name="Описание")
    link_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")

    class Meta:
        verbose_name = "Ссылка на GitHub"
        verbose_name_plural = "Ссылки на GitHub"

    def __str__(self):
        return self.title
