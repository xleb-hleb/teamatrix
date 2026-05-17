from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotLoaderConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eye_x', models.FloatField(default=0.08, verbose_name='Смещение X (доля maxDim)')),
                ('eye_y', models.FloatField(default=0.18, verbose_name='Смещение Y (доля maxDim)')),
                ('eye_z', models.FloatField(default=0.22, verbose_name='Смещение Z (доля maxDim)')),
                ('eye_size', models.FloatField(default=0.035, verbose_name='Размер глаза (доля maxDim)')),
                ('eye_intensity', models.FloatField(default=4.0, verbose_name='Яркость свечения')),
                ('eye_start_t', models.FloatField(default=0.72, verbose_name='Начало свечения (прогресс 0–1)')),
            ],
            options={
                'verbose_name': 'Настройки глаза робота',
                'verbose_name_plural': 'Настройки глаза робота',
            },
        ),
    ]
