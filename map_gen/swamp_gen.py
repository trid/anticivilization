__author__ = 'TriD'


def generate_swamp(game_map, midpoint, radius):
    """Temporary algorithm for generating swamps"""
    r_square = radius * radius
    for x in range(midpoint.x - radius, midpoint.x + radius):
        x_square = x * x
        for y in range(midpoint.y - radius, midpoint.y + radius):
            if x_square + y * y < r_square:
                game_map[x][y].ground = "swamp"