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

    @classmethod
    def open_room(cls, name, grid_size, game_difficulty):
        game = MinesweeperGame.start_game(grid_size, game_difficulty)
        
        return cls.objects.create(name=name, state=ROOM_OPEN, game=game)

    def close_room(self):
        self.state = ROOM_CLOSED
        self.save()


class MinesweeperGame(models.Model):
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    game_state = models.CharField()
    grid_size = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 31)])

    @classmethod
    def start_game(game, grid_size, difficulty):
        from mines.utils.build_game import build_grid

        # A difficulty map to translate semantic difficulty into average percentage of bombs on a field.
        difficulty_map = {
            'easy': 20,
            'medium': 40,
            'hard': 60
        }
        difficulty_value = difficulty_map.get(difficulty, 40)  # Default difficulty of Medium

        # Create a grid of <grid_size x grid_size> 
        grid = build_grid(grid_size, difficulty_value)

