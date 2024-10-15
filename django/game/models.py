from django.db import models
from player.models import Player

def set_ano():
    return Player.objects.get(username='anonymous')
# Create your models here.

class Game(models.Model):
    # id cree par django
    state = models.CharField(blank=True, null=True, max_length=30) # (waiting, pause, active, end)
    mode = models.CharField(blank=True, null=True, max_length=30)
    player1 = models.ForeignKey(Player, related_name='%(class)s_player1', on_delete=models.SET(set_ano), null=True, default=None) 
    player2 = models.ForeignKey(Player, related_name='%(class)s_player2', on_delete=models.SET(set_ano),  null=True, default=None) 
    scorep1 = models.IntegerField(default=0)
    scorep2 = models.IntegerField(default=0)

    # socketp1 = models.CharField(max_length=255, null=True, blank=True)
    # socketp2 = models.CharField(max_length=255, null=True, blank=True)
