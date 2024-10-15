from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import os

def upload_to_profile_pictures(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('profile_pictures', instance.username, filename)

class Player(AbstractUser):
    student = models.BooleanField(default=False)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    email = models.CharField(blank=True, null=True, max_length=40)
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_picture = models.TextField(null=True)
    #image_data_url = models.CharField(null=True)
    language = models.CharField(max_length=2, default="EN")
    socket = models.CharField(max_length=255, null=True, blank=True)

    email_2fa_active = models.BooleanField(default=False)
    sms_2fa_active = models.BooleanField(default=False)
    anonymized = models.BooleanField(default=False)

    rank = models.IntegerField(default=1000)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    balls_returned = models.IntegerField(default=0)

    moveUpP1 = models.CharField(blank=True, null=True, max_length=18, default="KeyW")
    moveUpP2 = models.CharField(blank=True, null=True, max_length=18, default="KeyS")
    moveDownP1 = models.CharField(blank=True, null=True, max_length=18, default="ArrowUp")
    moveDownP2 = models.CharField(blank=True, null=True, max_length=18, default="ArrowDown")
    pause = models.CharField(blank=True, null=True, max_length=18, default="KeyP")
    mute = models.CharField(blank=True, null=True, max_length=18, default="KeyM")

    def __str__(self):
        return self.username
    

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token