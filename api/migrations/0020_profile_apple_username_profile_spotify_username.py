# Generated by Django 4.0.5 on 2022-07-01 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0019_alter_mixtape_is_public"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="apple_username",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="profile",
            name="spotify_username",
            field=models.CharField(default="", max_length=255),
        ),
    ]
