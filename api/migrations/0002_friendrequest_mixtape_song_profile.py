# Generated by Django 4.0.5 on 2022-06-20 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FriendRequest",
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
            ],
        ),
        migrations.CreateModel(
            name="Mixtape",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=255)),
                ("is_public", models.BooleanField(default=False)),
                ("description", models.TextField()),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "favorited_by",
                    models.ManyToManyField(
                        blank=True,
                        related_name="favorite_mixtapes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Song",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("spotify_title", models.TextField()),
                ("spotify_artist", models.TextField()),
                ("spotify_album", models.TextField()),
                ("spotify_url", models.TextField()),
                ("apple_music_title", models.TextField()),
                ("apple_music_artist", models.TextField()),
                ("apple_music_album", models.TextField()),
                ("apple_music_url", models.TextField()),
                ("spotify_preview_url", models.TextField()),
                (
                    "favorited_by",
                    models.ManyToManyField(
                        related_name="favorite_songs", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "mixtapes",
                    models.ManyToManyField(
                        blank=True, related_name="mixtapes", to="api.mixtape"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("spotify_username", models.CharField(default="", max_length=255)),
                ("spotify_password", models.CharField(default="", max_length=255)),
                ("spotify_created_at", models.DateTimeField()),
                ("apple_music_username", models.CharField(default="", max_length=255)),
                ("apple_music_password", models.CharField(default="", max_length=255)),
                ("apple_music_created_at", models.DateTimeField()),
                (
                    "followers",
                    models.ManyToManyField(
                        related_name="followers", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
