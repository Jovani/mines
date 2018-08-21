from mines.models import GameRoom
from mines.serializers import GameRoomSerializer
from rest_framework import generics
from rest_framework.response import Response


class GameRoomCreate(generics.ListCreateAPIView):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomSerializer

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        grid_size = request.data['grid_size']
        difficulty = request.data['difficulty']

        GameRoom.open_room(
            name,
            int(grid_size),
            difficulty,
        )

        return Response(status=204)