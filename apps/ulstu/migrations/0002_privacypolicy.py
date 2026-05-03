from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ulstu", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PrivacyPolicy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(verbose_name="Текст политики конфиденциальности")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
            ],
            options={
                "verbose_name": "Политика конфиденциальности",
                "verbose_name_plural": "Политика конфиденциальности",
            },
        ),
    ]
