from rest_framework import serializers
from .models import Friendship, Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'nickname', 'rank', 'win', 'lose', 'last_login']  # Sélectionnez les champs nécessaires

class FriendSerializer(serializers.ModelSerializer):
    friend = PlayerSerializer(read_only=True)  # Sérialiser le joueur 1
    user = PlayerSerializer(read_only=True)  # Sérialiser le joueur 2

    class Meta:
        model = Friendship
        fields = ['user', 'friend', 'created_at']