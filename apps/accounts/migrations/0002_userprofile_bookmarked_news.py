from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="bookmarked_news",
            field=models.ManyToManyField(
                blank=True,
                to="core.news",
                verbose_name="Новости в закладках",
            ),
        ),
    ]
