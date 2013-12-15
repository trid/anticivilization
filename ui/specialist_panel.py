import pygame
from pygame.rect import Rect
from pygame.surface import Surface
from label import Label
import specialist
from ui.clickable import Clickable

__author__ = 'TriD'


#Let us make all specialist drawing routine simple
class SpecialistPanel(Clickable):
    def __init__(self, x, y, specialist_instance, selectable=False):
        self.surface = Surface((200, 60))
        self.specialist = specialist_instance
        self.s_type = Label(0, 0, specialist.mapping[specialist_instance.s_type])
        self.s_exp = Label(0, 40, "")
        self.s_level = Label(0, 20, "")
        self.selectable = selectable
        self.selected = False
        self.x = x
        self.y = y
        self.w = 200
        self.h = 60

    def draw(self, screen):
        self.surface.fill(0x000000)
        pygame.draw.rect(self.surface, 0xb7f315 if self.selected else 0xffffff, Rect(0, 0, 198, 58), 2)
        self.s_exp.set_text("Exp: %s/%s" % (self.specialist.experience, self.specialist.level_up_exp))
        self.s_level.set_text("Level: %s" % self.specialist.level)
        self.s_type.draw(self.surface)
        self.s_exp.draw(self.surface)
        self.s_level.draw(self.surface)
        screen.blit(self.surface, (self.x, self.y))

    def is_pressed(self, x, y):
        if not self.selectable:
            return False
        if x < self.x:
            return False
        elif x > self.x + self.w:
            return False
        elif y < self.y:
            return False
        elif y > self.y + self.h:
            return False

        if self.selectable:
            self.selected = not self.selected
