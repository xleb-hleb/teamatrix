from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subsystem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("description", models.TextField(verbose_name="Описание")),
                ("image", models.ImageField(blank=True, upload_to="development/subsystems/", verbose_name="Изображение")),
                ("icon", models.CharField(blank=True, default="bi-cpu", max_length=50, verbose_name="Bootstrap-иконка")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Подсистема",
                "verbose_name_plural": "Подсистемы",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Component",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subsystem", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="components", to="development.subsystem", verbose_name="Подсистема")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("specs", models.TextField(blank=True, verbose_name="Характеристики")),
                ("purpose", models.TextField(verbose_name="Назначение")),
                ("buy_url", models.URLField(blank=True, verbose_name="Ссылка для заказа")),
                ("image", models.ImageField(blank=True, upload_to="development/components/", verbose_name="Изображение")),
            ],
            options={
                "verbose_name": "Комплектующее",
                "verbose_name_plural": "Комплектующие",
            },
        ),
        migrations.CreateModel(
            name="ReadySolution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("url", models.URLField(blank=True, verbose_name="Ссылка")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Готовое решение",
                "verbose_name_plural": "Готовые решения",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="DevSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("content", models.TextField(verbose_name="Содержание")),
                ("icon", models.CharField(blank=True, default="bi-tools", max_length=50, verbose_name="Bootstrap-иконка")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Раздел разработки",
                "verbose_name_plural": "Разделы разработки",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="GitHubLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("url", models.URLField(verbose_name="Ссылка на GitHub")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("link_type", models.CharField(choices=[("models", "3D-модели"), ("software", "Программные решения")], max_length=20, verbose_name="Тип")),
            ],
            options={
                "verbose_name": "Ссылка на GitHub",
                "verbose_name_plural": "Ссылки на GitHub",
            },
        ),
    ]
