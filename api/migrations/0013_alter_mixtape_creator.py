# Generated by Django 4.0.5 on 2022-06-26 01:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_song_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mixtape',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mixtapes', to=settings.AUTH_USER_MODEL),
        ),
    ]
