'''
    Helper module for building a minesweeper game
'''

import random
from functools import reduce
from mines.utils import get_search_list


'''
    Helper methods for building the grid and setting the bombs
'''
def build_grid(grid_size, difficulty):
    # Build a grid of bombs and non-bombs
    base_grid = [build_row(grid_size, difficulty) for x in range(grid_size)]

    # With the bombs now set, go over the grid again and determine the values of the non-bomb squares
    return fill_grid(base_grid)

def build_row(grid_size, difficulty):
    return [build_column(grid_size, difficulty) for x in range(grid_size)]

def build_column(grid_size, difficulty):
    is_bomb = random.randrange(0, 100) < difficulty
    return {
        'flipped': False,
        'value': -1 if is_bomb else 0
    }

'''
    Helper methods for filling the values of non-bomb squares
'''
def fill_grid(base_grid):
    return [fill_column(base_grid, i, column) for i, column in enumerate(base_grid)]

def fill_column(base_grid, index, column):
    return [compute_square_value(base_grid, index, j, square) for j, square in enumerate(column)]

def compute_square_value(base_grid, index_i, index_j, square):
    # Each non-bomb square's value must be equal to the number of bombs surrounding it.
    if square['value'] == -1:
        return square

    # do a shallow copy of the square, to avoid mutating.
    new_square = dict(square)

    # Compute the square's value based on the number of surrounding bombs.
    value = reduce(
        lambda value, pair: value + 1 if is_bomb_square(base_grid, *pair) else value,
        get_search_list(index_i, index_j),
        0
    )

    new_square['value'] = value
    return new_square

def is_bomb_square(base_grid, x, y):
    if x < 0 or y < 0:
        return False
    
    try:
        other_square = base_grid[x][y]
    except IndexError:
        return False
    else:
        if other_square['value'] == -1:
            return True
