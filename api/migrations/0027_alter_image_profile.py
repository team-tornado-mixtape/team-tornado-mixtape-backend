# Generated by Django 4.0.5 on 2022-07-02 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_remove_profile_image_image_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='profile',
            field=models.ManyToManyField(blank=True, null=True, related_name='images', to='api.profile'),
        ),
    ]
