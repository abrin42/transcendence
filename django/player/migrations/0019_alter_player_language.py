# Generated by Django 5.0.6 on 2024-10-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0018_player_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='language',
            field=models.CharField(default='EN', max_length=2),
        ),
    ]
