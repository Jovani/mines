'''
    Generic helper functions
'''

# Helper function to get (up to) all 8 squares surrounding the given square
def get_search_list(x, y):
    return [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),

        (x, y - 1),
        (x, y + 1),

        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]