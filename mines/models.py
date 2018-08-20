import json
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
    name = models.CharField(max_length=100)
    state = models.CharField(choices=ROOM_STATE_CHOICES, max_length=6)
    game = models.OneToOneField(
        'MinesweeperGame',
        on_delete=models.CASCADE,
        related_name='room',
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
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=6)
    _game_state = models.TextField()
    grid_size = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 31)])

    @property
    def game_state(self):
        return json.loads(self._game_state)

    @game_state.setter
    def game_state(self, value):
        self._game_state = json.dumps(value)

    @classmethod
    def start_game(cls, grid_size, difficulty):
        from mines.utils.build_game import build_grid

        # A difficulty map to translate semantic difficulty into average percentage of bombs on a field.
        difficulty_map = {
            'easy': 20,
            'medium': 40,
            'hard': 60
        }
        difficulty_value = difficulty_map.get(difficulty, 40)  # Default difficulty of Medium

        # Create a grid of <grid_size x grid_size> 
        game_state = build_grid(grid_size, difficulty_value)

        # We invoke the MinesweeperGame directly in order to make use of our nifty game_state property
        game = cls(difficulty=difficulty, game_state=game_state, grid_size=grid_size)
        game.save()

        return game

    def flip_square(self, x, y, initial_flip):
        '''
            Flip a square.
            If it's a bomb, the player loses and the room must be closed.
            Otherwise, we have to then flip all non-bomb squares that are contiguous to this one, without triggering bombs.
        '''
        from mines.utils import get_search_list

        game_state = self.game_state
        square = game_state[x][y]
        
        if square['value'] == -1:
            if initial_flip:
                self.finish_game(win=False)

            return
        elif square['flipped']:
            return

        square['flipped'] = True
        self.game_state = game_state

        chain_trigger_list = get_search_list(x, y)
        for pair in chain_trigger_list:
            self.flip_square(*pair, False)
            

    def finish_game(self, win):
        self.reveal_all_bombs()
        self.room.state = ROOM_CLOSED
        self.room.save()

    def reveal_all_bombs(self):
        # TODO
        pass