from django.contrib.auth.models import AbstractUser
from django.db import models
#from django.utils import timezone
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
import os

def upload_to_profile_pictures(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('profile_pictures', instance.username, filename)

class Player(AbstractUser):
    student = models.BooleanField(default=False)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    date_joined = models.DateField(default=date.today)
    newpassword = models.CharField(blank=True, null=True, max_length=40)
    
    original_email = models.EmailField(blank=True, null=True, max_length=40)
    original_phone_number = PhoneNumberField(blank=True, null=True)
    email = models.CharField(blank=True, null=True, max_length=40)
    phone_number = PhoneNumberField(blank=True, null=True)

    profile_picture = models.TextField(null=True)
    language = models.CharField(max_length=2, default="EN")
    socket = models.CharField(max_length=255, null=True, blank=True)

    email_2fa_active = models.BooleanField(default=False)
    sms_2fa_active = models.BooleanField(default=False)
    anonymized = models.BooleanField(default=False)
    csrf = models.CharField(blank=True, null=True, max_length=150)

    rank = models.IntegerField(default=1000)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    balls_returned = models.IntegerField(default=0)

    player1Up = models.CharField(blank=True, null=True, max_length=18, default="KeyW")
    player1Down = models.CharField(blank=True, null=True, max_length=18, default="KeyS")
    player2Up = models.CharField(blank=True, null=True, max_length=18, default="ArrowUp")
    player2Down = models.CharField(blank=True, null=True, max_length=18, default="ArrowDown")
    pause = models.CharField(blank=True, null=True, max_length=18, default="KeyP")
    mute = models.CharField(blank=True, null=True, max_length=18, default="KeyM")

    def __str__(self):
        return self.username
    

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token