# Generated by Django 5.0.6 on 2024-09-23 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0017_alter_player_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='language',
            field=models.CharField(blank=True, default='EN', max_length=2, null=True),
        ),
    ]