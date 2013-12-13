import pygame
from pygame.rect import Rect

__author__ = 'TriD'


class Display():
    def __init__(self, game_data, uis):
        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        self.label_font = pygame.font.SysFont('monospace', 17)
        self.game_data = game_data
        self.uis = uis
        self.mouse_x, self.mouse_y = 0, 0

    def draw_sprite(self, x, y, sprite):
        if x + 32 <= 600:
            self.screen.blit(sprite, [x, y])
        elif 632 > x + 32 > 600:
            self.screen.blit(sprite, [x, y], Rect(0, 0, 600 - x, sprite.get_height()))

    def draw(self):
        self.screen.fill((0, 0, 0))

        for x in range(0, 20):
            for y in range(0, 20):
                # New, better rendering that draws part of map that is currently on screen
                mx = x + self.game_data.dx / 32
                my = y + self.game_data.dy / 32
                sx = x * 32 - self.game_data.dx % 32
                sy = y * 32 - self.game_data.dy % 32
                self.draw_sprite(sx, sy, self.uis.sprites[self.game_data.game_map[mx][my].ground])
                if self.game_data.game_map[mx][my].resource:
                    self.draw_sprite(sx, sy, self.uis.sprites[self.game_data.game_map[mx][my].resource])
                if self.game_data.game_map[mx][my].building == 'center':
                    self.draw_sprite(sx, sy - 64, self.uis.sprites['center'])
                elif self.game_data.game_map[mx][my].building:
                    self.draw_sprite(sx, sy, self.uis.sprites[self.game_data.game_map[mx][my].building])
        for expedition in self.game_data.expeditions:
            self.draw_sprite(expedition.x * 32 - self.game_data.dx, expedition.y * 32 - 28 - self.game_data.dy, self.uis.sprites['human'])

        self.draw_sprite(self.game_data.monster.x * 32 - self.game_data.dx, self.game_data.monster.y * 32 - self.game_data.dy, self.uis.sprites['monster'])

        if self.game_data.buttons_active:
            self.uis.draw_buttons(self.screen)

        population_label = self.label_font.render("Population: %d/%d" % (
        self.game_data.village.population, self.game_data.village.max_population), 1,
                                             (255, 255, 255))
        self.screen.blit(population_label, (600, 0))
        food_label = self.label_font.render("Food: %d(+%d)" % (
        self.game_data.village.food_stockpile, self.game_data.village.food_growth), 1, (255, 255, 255))
        self.screen.blit(food_label, (600, 20))
        wood_label = self.label_font.render("Wood: %d(+%d)" % (
        self.game_data.village.wood_stockpile, self.game_data.village.wood_increasing), 1,
                                       (255, 255, 255))
        self.screen.blit(wood_label, (600, 40))

        lighted_x = (self.mouse_x - self.game_data.dx % 32) / 32
        lighted_y = (self.mouse_y - self.game_data.dy % 32) / 32
        x_ = lighted_x * 32
        lighted_x = x_ - self.game_data.dx % 32
        y_ = lighted_y * 32
        lighted_y = y_ - self.game_data.dy % 32

        pygame.draw.rect(self.screen, 0x10ffaa, Rect(lighted_x, lighted_y, 32, 32))

        pygame.display.flip()