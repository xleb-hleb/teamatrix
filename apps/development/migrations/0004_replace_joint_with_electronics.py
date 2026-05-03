from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("development", "0003_robotbodypart_details"),
    ]

    operations = [
        migrations.DeleteModel(
            name="RobotJoint",
        ),
        migrations.CreateModel(
            name="RobotElectronics",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("purpose", models.CharField(max_length=255, verbose_name="Назначение")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "body_part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="electronics",
                        to="development.robotbodypart",
                        verbose_name="Часть тела",
                    ),
                ),
            ],
            options={
                "verbose_name": "Электроника / контроллер",
                "verbose_name_plural": "Электроника и контроллеры",
                "ordering": ["order"],
            },
        ),
    ]
