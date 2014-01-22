from point import Point

__author__ = 'TriD'


class GameSprite:
    def __init__(self, dx, dy, image):
        self.delta = Point(dx, dy)
        self.image = image

    def draw(self, point, screen):
        screen.blit(screen, (point.x + self.delta.x, point.y + self.delta.y))