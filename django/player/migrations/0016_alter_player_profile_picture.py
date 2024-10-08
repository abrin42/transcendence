# Generated by Django 5.0.7 on 2024-09-09 13:58

import player.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0015_alter_player_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/fallback.png', null=True, upload_to=player.models.upload_to_profile_pictures),
        ),
    ]
