import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RoadmapStage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Название этапа")),
                ("description", models.TextField(verbose_name="Описание")),
                ("period", models.CharField(max_length=100, verbose_name="Период (например: Q1 2025)")),
                ("is_completed", models.BooleanField(default=False, verbose_name="Завершён")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Этап дорожной карты",
                "verbose_name_plural": "Этапы дорожной карты",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="UlstuTeam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название команды")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Команда УлГТУ",
                "verbose_name_plural": "Команды УлГТУ",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="UlstuMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="members", to="ulstu.ulstuteam", verbose_name="Команда")),
                ("full_name", models.CharField(max_length=255, verbose_name="ФИО")),
                ("role", models.CharField(max_length=255, verbose_name="Роль")),
                ("bio", models.TextField(blank=True, verbose_name="О себе")),
                ("photo", models.ImageField(blank=True, upload_to="ulstu/members/", verbose_name="Фото")),
                ("email", models.EmailField(blank=True, verbose_name="Email")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Участник проекта УлГТУ",
                "verbose_name_plural": "Участники проекта УлГТУ",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Имя")),
                ("email", models.EmailField(verbose_name="Email")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="Телефон")),
                ("specialty", models.CharField(max_length=255, verbose_name="Специальность / направление")),
                ("motivation", models.TextField(verbose_name="Мотивация")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")),
                ("is_processed", models.BooleanField(default=False, verbose_name="Обработана")),
            ],
            options={
                "verbose_name": "Заявка на вступление",
                "verbose_name_plural": "Заявки на вступление",
                "ordering": ["-created_at"],
            },
        ),
    ]
