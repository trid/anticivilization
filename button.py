__author__ = 'TriD'


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def is_pressed(self, x, y):
        if x < self.x:
            return False
        elif x > self.x + self.w:
            return False
        elif y < self.y:
            return False
        elif y > self.y + self.h:
            return False
        return True