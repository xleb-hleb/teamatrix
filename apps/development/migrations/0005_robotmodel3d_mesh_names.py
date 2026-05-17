from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("development", "0004_replace_joint_with_electronics"),
    ]

    operations = [
        # Добавляем mesh_names к RobotBodyPart
        migrations.AddField(
            model_name="robotbodypart",
            name="mesh_names",
            field=models.TextField(
                blank=True,
                default="",
                help_text=(
                    "Через запятую — имена объектов/мешей в FBX-файле, "
                    "относящихся к этой части тела. "
                    "Используйте точные имена из редактора (Blender/Maya)."
                ),
                verbose_name="Имена мешей в FBX",
            ),
        ),
        # Создаём таблицу RobotModel3D
        migrations.CreateModel(
            name="RobotModel3D",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fbx_file",
                    models.FileField(
                        help_text="Загрузите файл модели в формате .fbx",
                        upload_to="development/robot3d/",
                        verbose_name="FBX-файл",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
            ],
            options={
                "verbose_name": "3D-модель робота (FBX)",
                "verbose_name_plural": "3D-модель робота (FBX)",
            },
        ),
    ]
