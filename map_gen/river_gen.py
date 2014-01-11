import random
import math
from game_map import MAP_WIDTH, SQUARE_WIDTH, SQUARE_HEIGHT, MAP_HEIGHT
from vector import Vector

__author__ = 'TriD'


def draw_river(vec, map):
    steep = math.fabs(vec.x2 - vec.x1) < math.fabs(vec.y2 - vec.y1)
    if steep:
        x2 = vec.y2
        x1 = vec.y1
        y2 = vec.x2
        y1 = vec.x1
    else:
        x2 = vec.x2
        x1 = vec.x1
        y2 = vec.y2
        y1 = vec.y1
    if x1 > x2:
        xt = x1
        x1 = x2
        x2 = xt
        yt = y1
        y1 = y2
        y2 = yt

    deltax = x2 - x1
    deltay = y2 - y1
    error = 0.
    deltaerr = math.fabs(deltay / deltax or 1)
    y = y1
    for x in range(x1, x2):
        if steep:
            map[y][x].ground = 'water'
            map[y + 1][x].ground = 'water'
            map[y - 1][x].ground = 'water'
        else:
            map[x][y].ground = 'water'
            map[x][y + 1].ground = 'water'
            map[x][y - 1].ground = 'water'
        error += deltaerr
        if error >= 0.5:
            y += 1
            error -= 1.0


def generate_rivers(map):
    width = MAP_WIDTH * SQUARE_WIDTH
    height = MAP_HEIGHT * SQUARE_HEIGHT

    for i in range(0, 20):
        draw_river(Vector(random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)), map)