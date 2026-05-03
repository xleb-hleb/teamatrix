from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotBodyPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(
                    choices=[
                        ('head', 'Голова'),
                        ('torso', 'Туловище'),
                        ('left_arm', 'Левая рука'),
                        ('right_arm', 'Правая рука'),
                        ('pelvis', 'Таз'),
                        ('left_leg', 'Левая нога'),
                        ('right_leg', 'Правая нога'),
                    ],
                    max_length=30,
                    unique=True,
                    verbose_name='Идентификатор части тела',
                )),
                ('label', models.CharField(max_length=100, verbose_name='Название')),
                ('progress', models.PositiveIntegerField(
                    default=0,
                    help_text='Целое число от 0 до 100',
                    verbose_name='Прогресс разработки (%)',
                )),
                ('subsystem', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='body_parts',
                    to='development.subsystem',
                    verbose_name='Связанная подсистема',
                )),
                ('description', models.TextField(blank=True, verbose_name='Описание (для всплывающего окна)')),
            ],
            options={
                'verbose_name': 'Часть тела робота',
                'verbose_name_plural': 'Части тела робота',
                'ordering': ['key'],
            },
        ),
    ]
