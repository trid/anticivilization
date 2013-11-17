__author__ = 'TriD'

import pygame
from tile import Tile
from village import Village
from ui_state import UIState

game_map = []

for i in range(0, 10):
    game_map.append([Tile() for k in range(0, 10)])

game_map[5][5].building = 'center'
game_map[9][9].resource = 'tree'

uis = UIState()

pygame.init()
screen = pygame.display.set_mode([800, 600])

done = False
buttons_active = False
buttons_pos = None

village = Village()

turn = 0

label_font = pygame.font.SysFont('monospace', 17)


def setup_buttons(buttons_pos):
    uis.button_homes.x = buttons_pos[0]
    uis.button_homes.y = buttons_pos[1]
    uis.button_fields.x = buttons_pos[0]
    uis.button_fields.y = buttons_pos[1] + 23


def build(mouse_x, mouse_y):
    x = mouse_x / 32
    y = mouse_y / 32

    may_build = False
    if game_map[x][y].building:
        return
    if x > 0:
        if game_map[x - 1][y].building:
            may_build = True
        if y > 0 and game_map[x - 1][y - 1].building:
            may_build = True
        if y < 9 and game_map[x - 1][y - 1].building:
            may_build = True
    if x < 9:
        if game_map[x + 1][y].building:
            may_build = True
        if y > 0 and game_map[x + 1][y - 1].building:
            may_build = True
        if y < 9 and game_map[x + 1][y + 1].building:
            may_build = True
    if y > 0 and game_map[x][y - 1].building:
        may_build = True
    if y < 9 and game_map[x][y + 1].building:
        may_build = True
    if may_build:
        game_map[x][y].building = uis.building


def next_turn():
    global village, turn
    turn += 1
    village.update_pop()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                buttons_active = True
                buttons_pos = event.pos
                setup_buttons(buttons_pos)
                building = None
            if event.button == 1:
                if buttons_active:
                    buttons_active = False
                    if uis.button_homes.is_pressed(event.pos[0], event.pos[1]):
                        uis.building = 'houses'
                    if uis.button_fields.is_pressed(event.pos[0], event.pos[1]):
                        uis.building = 'field'
                elif uis.building:
                    build(*event.pos)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                next_turn()

    screen.fill((0, 0, 0))

    for x in range(0, 10):
        for y in range(0, 10):
            screen.blit(uis.sprites[game_map[x][y].ground], [x * 32, y * 32])
            if game_map[x][y].resource:
                screen.blit(uis.sprites[game_map[x][y].resource], [x * 32, y * 32])
            if game_map[x][y].building == 'center':
                screen.blit(uis.sprites['center'], [x * 32, y * 32 - 64])
            elif game_map[x][y].building:
                screen.blit(uis.sprites[game_map[x][y].building], [x * 32, y * 32])

    if buttons_active:
        screen.blit(uis.sprites['build_homes'], buttons_pos)
        screen.blit(uis.sprites['build_field'], (buttons_pos[0], buttons_pos[1] + 23))

    population_label = label_font.render("Population: %d/%d" % (village.population, village.max_population), 1, (255, 255, 255))
    screen.blit(population_label, (320, 0))

    pygame.display.flip()