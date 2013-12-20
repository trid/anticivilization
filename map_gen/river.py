import random
from point import Point
from vector import Vector

__author__ = 'TriD'


class River:
    def __init__(self, x=0, y=0):
        self.start = Point(x, y)
        self.start_streams = []


class Stream:
    def __init__(self, parent):
        self.direction = Vector(parent.x1, parent.y1, random.randint(100) + parent.x1 + 5, random.randint(100) + parent.y1 + 5)
        self.branches = []

    def generate_branches(self):
        count = random.randint(0, 3)
        for i in range(0, count):
            self.branches.append(Stream(self))