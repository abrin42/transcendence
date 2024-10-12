from rest_framework import serializers
from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'status', 'created_at']
        depth = 1