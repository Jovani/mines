import random
from django.db import models


ROOM_OPEN = 'open'
ROOM_CLOSED = 'closed'

ROOM_STATE_CHOICES = (
    (ROOM_OPEN, 'Open'),
    (ROOM_CLOSED, 'Closed'),
)

DIFFICULTY_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


class GameRoom(models.Model):
    name = models.CharField()
    state = models.CharField(choices=ROOM_STATE_CHOICES)
    game = models.OneToOneField(
        'MinesweeperGame',
        on_delete=models.CASCADE,
        related_name='game_room',
    )

    created = models.DateTimeField(auto_now_add=True)

class MinesweeperGame(models.Model):
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    game_state = models.CharField()
    grid_size = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 31)])
