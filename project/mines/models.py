import json
from django.db import models


class GameRoom(models.Model):
    ROOM_OPEN = 'open'
    ROOM_CLOSED = 'closed'

    ROOM_STATE_CHOICES = (
        (ROOM_OPEN, 'Open'),
        (ROOM_CLOSED, 'Closed'),
    )

    name = models.CharField(max_length=100)
    state = models.CharField(choices=ROOM_STATE_CHOICES, default=ROOM_OPEN, max_length=6)
    game = models.OneToOneField(
        'MinesweeperGame',
        on_delete=models.CASCADE,
        related_name='room',
    )

    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def open_room(cls, name, grid_size, game_difficulty):
        game = MinesweeperGame.start_game(grid_size, game_difficulty)

        room = cls(name=name, game=game)
        room.clean_fields()
        room.save()

        return room

    def close_room(self):
        self.state = self.ROOM_CLOSED
        self.save()


class MinesweeperGame(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    DEFAULT_DIFFICULTY = MEDIUM

    DIFFICULTY_CHOICES = (
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    )

    GAME_OPEN = 'open'
    GAME_WON = 'won'
    GAME_LOST = 'lost'

    GAME_STATE_CHOICES = (
        (GAME_OPEN, 'Open'),
        (GAME_WON, 'Won'),
        (GAME_LOST, 'Lost')
    )

    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=6)
    _game_state = models.TextField(blank=True)
    grid_size = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 31)])
    state = models.CharField(choices=GAME_STATE_CHOICES, default=GAME_OPEN, max_length=4)

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
        difficulty_value = difficulty_map[difficulty]

        # Create a grid of <grid_size x grid_size> 
        game_state = build_grid(grid_size, difficulty_value)

        # We invoke the MinesweeperGame directly in order to make use of our nifty game_state property
        game = cls(difficulty=difficulty, game_state=game_state, grid_size=grid_size)
        
        # Ensure that fields are clean, and save.
        game.clean_fields()
        game.save()

        return game

    def flip_squares_and_save(self, x, y):
        self.flip_square(x, y, initial_flip=True)
        self.save()

    def flip_square(self, x, y, initial_flip):
        '''
            Flip a square.
            If it's a bomb, the player loses and the room must be closed.
            Otherwise, we have to then flip all non-bomb squares that are contiguous to this one, without triggering bombs.
        '''
        from mines.utils import get_search_list

        if x < 0 or y < 0:
            return

        game_state = self.game_state
        try:
            square = game_state[x][y]
        except IndexError:
            return
        
        # If the square is a bomb and this is the initial flip, the game ends in a loss.
        if square['value'] == -1:
            if initial_flip:
                self.finish_game_and_save(win=False)

            return
        elif square['flipped']:
            return

        # Flip the square and commit the changes into the game state, then flip surrounding non-bomb squares.
        square['flipped'] = True
        self.game_state = game_state

        chain_trigger_list = get_search_list(x, y)
        for pair in chain_trigger_list:
            self.flip_square(*pair, initial_flip=False)

    def finish_game_and_save(self, win):
        self.reveal_all_bombs()
        self.state = self.GAME_WON if win else self.GAME_LOST
        self.save()

        self.room.close_room()

    def reveal_all_bombs(self):
        game_state = self.game_state

        for row in game_state:
            gen = (square for square in row if square['value'] == -1)
            for square in gen:
                square['flipped'] = True

        self.game_state = game_state
