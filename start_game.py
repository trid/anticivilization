from pygame.rect import Rect
from GameData import GameData
from events import EventProcessor
__author__ = 'TriD'

import pygame
from ui_state import UIState

game_data = GameData()
uis = UIState(game_data)
game_data.uis = uis

event_processor = EventProcessor(game_data, uis)

pygame.init()
screen = pygame.display.set_mode([800, 600])

done = False
buttons_active = False
buttons_pos = None

turn = 0

label_font = pygame.font.SysFont('monospace', 17)

old_dx = 0
old_dy = 0
dx = 0
dy = 0
drag = False


def build_houses():
    uis.building = 'houses'


def build_field():
    uis.building = 'field'


def build_woodcutter():
    uis.building = 'woodcutter'


def send_expedition_callback():
    game_data.send_expedition()

uis.button_homes.callback = build_houses
uis.button_fields.callback = build_field
uis.button_woodcutter.callback = build_woodcutter
uis.button_expedition.callback = send_expedition_callback


def draw(x, y, sprite):
    global dx
    if x + 32 <= 600:
        screen.blit(sprite, [x, y])
    elif 632 > x + 32 > 600:
        screen.blit(sprite, [x, y], Rect(0, 0, 600 - x, sprite.get_height()))


while not game_data.done:
    event_processor.process_events()
    screen.fill((0, 0, 0))

    for x in range(0, 20):
        for y in range(0, 20):
            # New, better rendering that draws part of map that is currently on screen
            mx = x + game_data.dx / 32
            my = y + game_data.dy / 32
            sx = x * 32 - game_data.dx % 32
            sy = y * 32 - game_data.dy % 32
            draw(sx, sy, uis.sprites[game_data.game_map[mx][my].ground])
            if game_data.game_map[mx][my].resource:
                draw(sx, sy, uis.sprites[game_data.game_map[mx][my].resource])
            if game_data.game_map[mx][my].building == 'center':
                draw(sx, sy - 64, uis.sprites['center'])
            elif game_data.game_map[mx][my].building:
                draw(sx, sy, uis.sprites[game_data.game_map[mx][my].building])
    for expedition in game_data.expeditions:
        draw(expedition.x * 32 - dx, expedition.y * 32 - 28 - dy, uis.sprites['human'])

    draw(game_data.monster.x * 32 - game_data.dx, game_data.monster.y * 32 - game_data.dy, uis.sprites['monster'])

    if game_data.buttons_active:
        uis.draw_buttons(screen)

    population_label = label_font.render("Population: %d/%d" % (game_data.village.population, game_data.village.max_population), 1,
                                         (255, 255, 255))
    screen.blit(population_label, (600, 0))
    food_label = label_font.render("Food: %d(+%d)" % (game_data.village.food_stockpile, game_data.village.food_growth), 1, (255, 255, 255))
    screen.blit(food_label, (600, 20))
    wood_label = label_font.render("Wood: %d(+%d)" % (game_data.village.wood_stockpile, game_data.village.wood_increasing), 1,
                                   (255, 255, 255))
    screen.blit(wood_label, (600, 40))

    pygame.display.flip()