import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("author", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="blog_posts", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("summary", models.TextField(verbose_name="Краткое описание")),
                ("content", models.TextField(verbose_name="Содержание")),
                ("image", models.ImageField(blank=True, upload_to="blog/", verbose_name="Изображение")),
                ("tags", models.ManyToManyField(blank=True, related_name="posts", to="blog.tag", verbose_name="Теги")),
                ("is_published", models.BooleanField(default=False, verbose_name="Опубликовано")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
            ],
            options={
                "verbose_name": "Пост блога",
                "verbose_name_plural": "Посты блога",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog.blogpost", verbose_name="Пост")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blog_comments", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("content", models.TextField(verbose_name="Текст комментария")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("is_approved", models.BooleanField(default=True, verbose_name="Одобрен")),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
                "ordering": ["created_at"],
            },
        ),
    ]
