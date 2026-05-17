from django.db import migrations, models


def reset_to_pixel_defaults(apps, schema_editor):
    RobotLoaderConfig = apps.get_model('core', 'RobotLoaderConfig')
    RobotLoaderConfig.objects.filter(pk=1).update(eye_x=0.0, eye_y=0.0, eye_size=25.0)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_robotloaderconfig_intensity_remap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robotloaderconfig',
            name='eye_z',
        ),
        migrations.AlterField(
            model_name='robotloaderconfig',
            name='eye_x',
            field=models.FloatField(default=0.0, verbose_name='Смещение X (пиксели, вправо +)'),
        ),
        migrations.AlterField(
            model_name='robotloaderconfig',
            name='eye_y',
            field=models.FloatField(default=0.0, verbose_name='Смещение Y (пиксели, вверх +)'),
        ),
        migrations.AlterField(
            model_name='robotloaderconfig',
            name='eye_size',
            field=models.FloatField(default=25.0, verbose_name='Радиус кольца (пиксели)'),
        ),
        migrations.RunPython(reset_to_pixel_defaults, migrations.RunPython.noop),
    ]
