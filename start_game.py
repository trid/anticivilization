from expedition import Expedition
from monster import Monster

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
expedition = None
monster = Monster()

turn = 0

label_font = pygame.font.SysFont('monospace', 17)


def set_building(x, y):
    if uis.building == 'field':
        village.food_growth += 600
    elif uis.building == 'houses':
        village.max_population += 400
    elif uis.building == 'woodcutter':
        if game_map[x][y].resource != 'tree':
            return
        else:
            village.wood_increasing += 100
    game_map[x][y].building = uis.building


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
        set_building(x, y)


def next_turn():
    global village, turn
    turn += 1
    village.update()
    global expedition
    if expedition:
        expedition.move()
        if expedition.returned:
            expedition = None
            village.wood_stockpile += 100
    monster.random_move()


def send_expedition():
    global expedition
    if village.food_stockpile >= 100:
        expedition = Expedition()
        expedition.find_path(5, 5, exp_pos[0] / 32, exp_pos[1] / 32)
        village.food_stockpile -= 100


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                buttons_active = True
                buttons_pos = event.pos
                uis.setup_buttons(*buttons_pos)
                if game_map[buttons_pos[0]/32][buttons_pos[1]/32].resource:
                    uis.set_resource_click_buttons()
                    exp_pos = buttons_pos
                else:
                    uis.set_grass_click()
                building = None
            if event.button == 1:
                if buttons_active:
                    buttons_active = False
                    if uis.button_homes.is_pressed(event.pos[0], event.pos[1]):
                        uis.building = 'houses'
                    if uis.button_fields.is_pressed(event.pos[0], event.pos[1]):
                        uis.building = 'field'
                    if uis.button_woodcutter.is_pressed(*event.pos):
                        uis.building = 'woodcutter'
                    if uis.button_expedition.is_pressed(event.pos[0], event.pos[1]):
                        send_expedition()
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
            if game_map[x][y].building:
                screen.blit(uis.sprites[game_map[x][y].building], [x * 32, y * 32])
    if expedition:
        screen.blit(uis.sprites['human'], (expedition.x * 32, expedition.y * 32 - 28))

    screen.blit(uis.sprites['monster'], (monster.x * 32, monster.y * 32))

    if buttons_active:
        uis.draw_buttons(screen)

    population_label = label_font.render("Population: %d/%d" % (village.population, village.max_population), 1, (255, 255, 255))
    screen.blit(population_label, (320, 0))
    food_label = label_font.render("Food: %d(+%d)" % (village.food_stockpile, village.food_growth), 1, (255, 255, 255))
    screen.blit(food_label, (320, 20))
    wood_label = label_font.render("Wood: %d(+%d)" % (village.wood_stockpile, village.wood_increasing), 1, (255, 255, 255))
    screen.blit(wood_label, (320, 40))

    pygame.display.flip()