from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EquipmentCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("icon", models.CharField(blank=True, default="bi-box", max_length=50, verbose_name="Bootstrap-иконка")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Категория оборудования",
                "verbose_name_plural": "Категории оборудования",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="materials", to="equipment.equipmentcategory", verbose_name="Категория")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("properties", models.TextField(blank=True, verbose_name="Характеристики")),
                ("image", models.ImageField(blank=True, upload_to="equipment/materials/", verbose_name="Изображение")),
            ],
            options={
                "verbose_name": "Материал",
                "verbose_name_plural": "Материалы",
            },
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("url", models.URLField(blank=True, verbose_name="Сайт")),
                ("country", models.CharField(blank=True, max_length=100, verbose_name="Страна")),
                ("categories", models.ManyToManyField(blank=True, related_name="suppliers", to="equipment.equipmentcategory", verbose_name="Категории")),
                ("image", models.ImageField(blank=True, upload_to="equipment/suppliers/", verbose_name="Логотип")),
            ],
            options={
                "verbose_name": "Поставщик / Фабрика",
                "verbose_name_plural": "Поставщики / Фабрики",
            },
        ),
    ]
