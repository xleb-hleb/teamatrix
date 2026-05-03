import apps.cloud.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CloudFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("original_name", models.CharField(max_length=255, verbose_name="Имя файла")),
                (
                    "file",
                    models.FileField(
                        storage=apps.cloud.models.cloud_storage,
                        upload_to=apps.cloud.models._cloud_upload_path,
                        verbose_name="Файл",
                    ),
                ),
                ("size", models.BigIntegerField(default=0, verbose_name="Размер (байт)")),
                ("mime_type", models.CharField(blank=True, max_length=100, verbose_name="MIME-тип")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата загрузки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Файл",
                "verbose_name_plural": "Файлы",
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
