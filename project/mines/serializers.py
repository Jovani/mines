from rest_framework import serializers
from mines.models import GameRoom, MinesweeperGame


class GameRoomSerializer(serializers.ModelSerializer):
    grid_size = serializers.IntegerField(source='game.grid_size')
    difficulty = serializers.CharField(source='game.difficulty')
    game_id = serializers.IntegerField(source='game.id')

    class Meta:
        model = GameRoom
        fields = ('id', 'name', 'state', 'grid_size', 'difficulty', 'game_id')

class MinesweeperGameSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name')
    obscured_game_state = serializers.CharField()

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'room_name', 'state', 'obscured_game_state')
