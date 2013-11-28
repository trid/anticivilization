from pygame.rect import Rect
from expedition import Expedition
from game_map import GameMap
from monster import Monster

__author__ = 'TriD'

import pygame
from village import Village
from ui_state import UIState

game_map = GameMap()

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

old_dx = 0
old_dy = 0
dx = 0
dy = 0
drag = False


def send_expedition():
    global expedition
    if village.food_stockpile >= 100:
        expedition = Expedition()
        expedition.find_path(5, 5, exp_pos[0], exp_pos[1])
        village.food_stockpile -= 100


def build_houses():
    uis.building = 'houses'


def build_field():
    uis.building = 'field'


def build_woodcutter():
    uis.building = 'woodcutter'


def send_expedition_callback():
    send_expedition()

uis.button_homes.callback = build_houses
uis.button_fields.callback = build_field
uis.button_woodcutter.callback = build_woodcutter
uis.button_expedition.callback = send_expedition_callback

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
    x = (mouse_x - dx - dx % 32) / 32
    y = (mouse_y - dy - dy % 32) / 32

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


def draw(x, y, sprite):
    global dx
    if x + 32 <= 600:
        screen.blit(sprite, [x, y])
    elif 632 > x + 32 > 600:
        screen.blit(sprite, [x, y], Rect(0, 0, 600 - x, sprite.get_height()))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                buttons_active = True
                buttons_pos = event.pos
                uis.setup_buttons(*buttons_pos)
                if game_map[(buttons_pos[0] + dx - dx % 32) / 32][(buttons_pos[1] + dy - dy % 32) / 32].resource:
                    uis.set_resource_click_buttons()
                    exp_pos = ((buttons_pos[0] + dx - dx % 32) / 32, (buttons_pos[1] + dy - dy % 32) / 32)
                else:
                    uis.set_grass_click()
                building = None
            if event.button == 1:
                if buttons_active:
                    buttons_active = False
                    uis.process_buttons(*event.pos)
                elif uis.building:
                    build(*event.pos)
                if drag:
                    drag = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                next_turn()
        if event.type == pygame.MOUSEMOTION and drag:
            #And here we move the map on the screen
            mouse_pos_x, mouse_pos_y = event.pos
            dx = old_dx + (mouse_pos_x - mouse_drag_x)
            dy = old_dy + (mouse_pos_y - mouse_drag_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #Here we start drag the map
                drag = True
                mouse_drag_x, mouse_drag_y = event.pos
                old_dx = dx
                old_dy = dy

    screen.fill((0, 0, 0))

    for x in range(0, 20):
        for y in range(0, 20):
            # New, better rendering that draws part of map that is currently on screen
            mx = x + dx / 32
            my = y + dy / 32
            sx = x * 32 - dx % 32
            sy = y * 32 - dy % 32
            draw(sx, sy, uis.sprites[game_map[mx][my].ground])
            if game_map[mx][my].resource:
                draw(sx, sy, uis.sprites[game_map[mx][my].resource])
            if game_map[mx][my].building == 'center':
                draw(sx, sy - 64, uis.sprites['center'])
            elif game_map[mx][my].building:
                draw(sx, sy, uis.sprites[game_map[mx][my].building])
    if expedition:
        draw(expedition.x * 32 - dx, expedition.y * 32 - 28 - dy, uis.sprites['human'])

    draw(monster.x * 32 - dx, monster.y * 32 - dy, uis.sprites['monster'])

    if buttons_active:
        uis.draw_buttons(screen)

    population_label = label_font.render("Population: %d/%d" % (village.population, village.max_population), 1,
                                         (255, 255, 255))
    screen.blit(population_label, (600, 0))
    food_label = label_font.render("Food: %d(+%d)" % (village.food_stockpile, village.food_growth), 1, (255, 255, 255))
    screen.blit(food_label, (600, 20))
    wood_label = label_font.render("Wood: %d(+%d)" % (village.wood_stockpile, village.wood_increasing), 1,
                                   (255, 255, 255))
    screen.blit(wood_label, (600, 40))

    pygame.display.flip()