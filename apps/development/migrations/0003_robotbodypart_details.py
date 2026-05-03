from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0002_robotbodypart'),
    ]

    operations = [
        # Add new fields to RobotBodyPart
        migrations.AddField(
            model_name='robotbodypart',
            name='color',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Например: #00d4ff или rgba(0,212,255,0.8)',
                max_length=30,
                verbose_name='Цвет (CSS)',
            ),
        ),
        migrations.AddField(
            model_name='robotbodypart',
            name='controllers',
            field=models.TextField(
                blank=True,
                help_text='Описание CAN-шины, моторных контроллеров, бортового ПК и т.д.',
                verbose_name='Контроллеры и электроника',
            ),
        ),

        # RobotJoint
        migrations.CreateModel(
            name='RobotJoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joint_index', models.PositiveSmallIntegerField(verbose_name='Индекс сустава')),
                ('joint_name', models.CharField(max_length=100, verbose_name='Название сустава')),
                ('can_id', models.PositiveSmallIntegerField(verbose_name='CAN ID')),
                ('can_bus', models.CharField(help_text='Например: CAN0, CAN1', max_length=20, verbose_name='CAN-шина')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('body_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='joints',
                    to='development.robotbodypart',
                    verbose_name='Часть тела',
                )),
            ],
            options={
                'verbose_name': 'Сустав',
                'verbose_name_plural': 'Суставы',
                'ordering': ['order', 'joint_index'],
            },
        ),

        # RobotBOMItem
        migrations.CreateModel(
            name='RobotBOMItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('quantity', models.CharField(help_text='Например: 5, по BOM, набор', max_length=50, verbose_name='Количество')),
                ('acquisition', models.CharField(help_text='Например: Купить, Печать, Сборка', max_length=50, verbose_name='Способ получения')),
                ('material', models.CharField(blank=True, max_length=100, verbose_name='Материал/тип')),
                ('note', models.TextField(blank=True, verbose_name='Примечание')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('body_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='bom_items',
                    to='development.robotbodypart',
                    verbose_name='Часть тела',
                )),
            ],
            options={
                'verbose_name': 'BOM-позиция',
                'verbose_name_plural': 'BOM-позиции',
                'ordering': ['order'],
            },
        ),

        # RobotDrawing
        migrations.CreateModel(
            name='RobotDrawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Подпись')),
                ('url', models.URLField(verbose_name='Ссылка на CAD / файл')),
                ('source', models.CharField(blank=True, help_text='Например: Onshape, MakerWorld', max_length=100, verbose_name='Источник')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('body_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='drawings',
                    to='development.robotbodypart',
                    verbose_name='Часть тела',
                )),
            ],
            options={
                'verbose_name': 'CAD-чертёж / модель',
                'verbose_name_plural': 'CAD-чертежи / модели',
                'ordering': ['order'],
            },
        ),

        # RobotReference
        migrations.CreateModel(
            name='RobotReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Подпись')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('body_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='references',
                    to='development.robotbodypart',
                    verbose_name='Часть тела',
                )),
            ],
            options={
                'verbose_name': 'Справочная ссылка',
                'verbose_name_plural': 'Справочные ссылки',
                'ordering': ['order'],
            },
        ),

        # RobotAssemblyStep
        migrations.CreateModel(
            name='RobotAssemblyStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название шага')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('body_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='assembly_steps',
                    to='development.robotbodypart',
                    verbose_name='Часть тела',
                )),
            ],
            options={
                'verbose_name': 'Этап сборки',
                'verbose_name_plural': 'Этапы сборки',
                'ordering': ['order'],
            },
        ),
    ]
