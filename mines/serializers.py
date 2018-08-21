from rest_framework import serializers
from mines.models import GameRoom, MinesweeperGame


class GameRoomSerializer(serializers.ModelSerializer):
    grid_size = serializers.IntegerField(source='game.grid_size')
    difficulty = serializers.CharField(source='game.difficulty')

    class Meta:
        model = GameRoom
        fields = ('id', 'name', 'state', 'grid_size', 'difficulty')
