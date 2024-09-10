from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import os

def upload_to_profile_pictures(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('profile_pictures', instance.username, filename)

class Player(AbstractUser):
    profile_picture = models.ImageField(upload_to=upload_to_profile_pictures, blank=True, null=False, default="profile_pictures/fallback.png")
    rank = models.IntegerField(default=1000)
    phone_number = PhoneNumberField(blank=True, null=True)

    email_2fa_active = models.BooleanField(default=False)
    sms_2fa_active = models.BooleanField(default=False)
    student = models.BooleanField(default=False)

    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    nickname = models.CharField(blank=True, null=True, max_length=30)

    def __str__(self):
        return self.username
    

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
