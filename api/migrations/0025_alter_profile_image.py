# Generated by Django 4.0.5 on 2022-07-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_image_profile_remove_image_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, related_name='profiles', to='api.image'),
        ),
    ]