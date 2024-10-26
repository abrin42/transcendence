from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        # Tous les champs du modèle Player à inclure dans la réponse JSON
        fields = [
            'id', 'username',
        ]
