from django.db import migrations, models


def remap_intensity(apps, schema_editor):
    """Reset intensity to 1.0 (new scale: multiplier) for any existing singleton record."""
    RobotLoaderConfig = apps.get_model('core', 'RobotLoaderConfig')
    RobotLoaderConfig.objects.filter(pk=1).update(eye_intensity=1.0)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_robotloaderconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotloaderconfig',
            name='eye_intensity',
            field=models.FloatField(default=1.0, verbose_name='Яркость свечения (0–2)'),
        ),
        migrations.RunPython(remap_intensity, migrations.RunPython.noop),
    ]
