from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("development", "0005_robotmodel3d_mesh_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="robotbodypart",
            name="annotation_x",
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name="Аннотация X",
                help_text="3D-координата точки привязки аннотации (задаётся через инструмент разметки)",
            ),
        ),
        migrations.AddField(
            model_name="robotbodypart",
            name="annotation_y",
            field=models.FloatField(blank=True, null=True, verbose_name="Аннотация Y"),
        ),
        migrations.AddField(
            model_name="robotbodypart",
            name="annotation_z",
            field=models.FloatField(blank=True, null=True, verbose_name="Аннотация Z"),
        ),
    ]
