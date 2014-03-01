from pygame.rect import Rect
from button import Button

__author__ = 'TriD'


class RadioButton(Button):
    def __init__(self, x, y, w, h, sprite=None):
        Button.__init__(self, x, y, w, h, sprite=sprite)
        self.checked = False

    def draw(self, screen):
        if not self.checked:
            screen.blit(self.sprite, (self.x, self.y), Rect(0, 0, self.sprite.get_width(), self.sprite.get_height()/2))
        else:
            screen.blit(self.sprite, (self.x, self.y), Rect(0, self.sprite.get_height()/2, self.sprite.get_width(), self.sprite.get_height()/2))

    def is_pressed(self, x, y):
        result = Button.is_pressed(self, x, y)
        if result:
            self.checked = not self.checked