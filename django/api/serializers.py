from rest_framework import serializers
from player.models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
