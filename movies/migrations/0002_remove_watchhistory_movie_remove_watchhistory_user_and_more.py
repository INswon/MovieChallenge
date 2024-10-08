# Generated by Django 5.1 on 2024-09-08 11:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="watchhistory",
            name="movie",
        ),
        migrations.RemoveField(
            model_name="watchhistory",
            name="user",
        ),
        migrations.CreateModel(
            name="UserMovieRecord",
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
                ("title", models.CharField(max_length=200)),
                ("poster", models.ImageField(upload_to="posters/")),
                ("date_watched", models.DateField()),
                ("rating", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Movie",
        ),
        migrations.DeleteModel(
            name="WatchHistory",
        ),
    ]
