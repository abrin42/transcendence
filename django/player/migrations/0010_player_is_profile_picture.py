# Generated by Django 5.0.6 on 2024-09-06 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_alter_player_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_profile_picture',
            field=models.BooleanField(default=False),
        ),
    ]
