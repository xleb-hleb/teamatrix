from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("description", models.TextField(verbose_name="Описание")),
                ("location", models.CharField(blank=True, max_length=255, verbose_name="Место проведения")),
                ("date", models.DateField(verbose_name="Дата начала")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="Дата окончания")),
                ("url", models.URLField(blank=True, verbose_name="Ссылка на мероприятие")),
                ("image", models.ImageField(blank=True, upload_to="events/", verbose_name="Изображение")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активно")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
            ],
            options={
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
                "ordering": ["date"],
            },
        ),
    ]
