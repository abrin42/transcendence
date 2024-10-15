from django.db import models
from player.models import Player

def set_ano():
    return Player.objects.get(username="anonymous")

class Friendship(models.Model):
    user = models.ForeignKey(Player, related_name='%(class)s_user1', on_delete=models.SET(set_ano))
    friend = models.ForeignKey(Player, related_name='%(class)s_player',  on_delete=models.SET(set_ano))

    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
    
    def __str__(self):
        return self.user.username + ' ' + self.friend.username + ' ' + self.status
    
    def userInfo(self):
        return {
        "username": self.user.username,
        "nickname": self.user.nickname,
        }
        
    def friendInfo(self):
        return {
            "username": self.friend.username,
            "nickname": self.friend.nickname,
        }