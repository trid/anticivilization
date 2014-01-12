__author__ = 'TriD'

import random


class Monster:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.environment = 'ground'

    def random_move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)