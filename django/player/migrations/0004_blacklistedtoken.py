# Generated by Django 4.2 on 2024-08-24 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_alter_player_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
                ('blacklisted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
