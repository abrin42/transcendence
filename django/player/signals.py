from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Player

#######################################################
#######################################################

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(pre_delete, sender=User)
def anonymize_user_data(sender, instance, **kwargs):
    instance.username = f'deleted_user_{instance.id}'
    instance.email = ''
    instance.first_name = ''
    instance.last_name = ''
    instance.save()

#######################################################
#######################################################
#######################################################

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.Player.save()