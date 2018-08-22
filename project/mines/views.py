
import json
from mines.models import GameRoom, MinesweeperGame
from mines.serializers import GameRoomSerializer, MinesweeperGameSerializer
from rest_framework import generics
from rest_framework.response import Response


class GameRoomCreate(generics.ListCreateAPIView):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomSerializer

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        grid_size = request.data['grid_size']
        difficulty = request.data['difficulty']

        room = GameRoom.open_room(
            name,
            int(grid_size),
            difficulty,
        )

        return Response(json.dumps({'id': room.game.id}))

class OpenGameRoom(generics.ListAPIView):
    queryset = GameRoom.objects.filter(state=GameRoom.ROOM_OPEN)
    serializer_class = GameRoomSerializer


class MinesweeperGameRetrieve(generics.RetrieveAPIView):
    serializer_class = MinesweeperGameSerializer
    queryset = MinesweeperGame.objects.all()
    lookup_field = 'id'
