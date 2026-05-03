import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Удаляем старые модели блога
        migrations.DeleteModel(name="Comment"),
        migrations.DeleteModel(name="BlogPost"),
        migrations.DeleteModel(name="Tag"),

        # Создаём новые модели форума
        migrations.CreateModel(
            name="Thread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("views_count", models.PositiveIntegerField(default=0, verbose_name="Просмотры")),
                ("is_pinned", models.BooleanField(default=False, verbose_name="Закреплено")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="forum_threads", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("article", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="forum_threads", to="articles.article", verbose_name="Статья")),
            ],
            options={
                "verbose_name": "Тема",
                "verbose_name_plural": "Темы",
                "ordering": ["-is_pinned", "-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="Удалено")),
                ("thread", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posts", to="blog.thread", verbose_name="Тема")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="forum_posts", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("reply_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="replies", to="blog.post", verbose_name="Ответ на")),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["created_at"],
            },
        ),
    ]
