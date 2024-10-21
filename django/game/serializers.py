from rest_framework import serializers
from .models import Game, Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'nickname', 'rank', 'win', 'lose', 'profile_picture']  # Sélectionnez les champs nécessaires

class GameSerializer(serializers.ModelSerializer):
    player1 = PlayerSerializer()  # Sérialiser le joueur 1
    player2 = PlayerSerializer()  # Sérialiser le joueur 2

    class Meta:
        model = Game
        fields = ['id', 'state', 'player1', 'player2', 'scorep1', 'scorep2']