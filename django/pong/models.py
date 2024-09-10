from django.db import models

# Create your models here.

class Game(models.Model):
    bar = models.FloatField(default=13)
    