__author__ = 'TriD'

import pygame
from button import Button

game_map = []

for i in range(0, 10):
    game_map.append(['grass' for k in range(0, 10)])

game_map[5][5] = 'center'

current_building = None

pygame.init()
screen = pygame.display.set_mode([800, 600])
sprites = {'center': pygame.image.load('res/images/center.png'),
           'grass': pygame.image.load('res/images/grass.png'),
           'build_homes': pygame.image.load('res/images/build_homes.png'),
           'build_field': pygame.image.load('res/images/build_field.png'),
           'houses': pygame.image.load('res/images/houses.png'),
           'field': pygame.image.load('res/images/field.png')}
done = False
buttons_active = False
buttons_pos = None
button_homes = Button(0, 0, 115, 23)
button_fields = Button(0, 0, 93, 23)
building = None


def setup_buttons(buttons_pos):
    button_homes.x = buttons_pos[0]
    button_homes.y = buttons_pos[1]
    button_fields.x = buttons_pos[0]
    button_fields.y = buttons_pos[1] + 23

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
                    if button_homes.is_pressed(event.pos[0], event.pos[1]):
                        building = 'houses'
                    if button_fields.is_pressed(event.pos[0], event.pos[1]):
                        building = 'field'
                elif building:
                    pos = event.pos
                    x = pos[0]/32
                    y = pos[1]/32
                    game_map[x][y] = building

    for x in range(0, 10):
        for y in range(0, 10):
            if game_map[x][y] != 'center':
                screen.blit(sprites['grass'], [x * 32, y * 32])
                screen.blit(sprites[game_map[x][y]], [x * 32, y * 32])
            else:
                screen.blit(sprites['grass'], [x * 32, y * 32])
                screen.blit(sprites['center'], [x * 32, y * 32 - 64])

    if buttons_active:
        screen.blit(sprites['build_homes'], buttons_pos)
        screen.blit(sprites['build_field'], (buttons_pos[0], buttons_pos[1] + 23))

    pygame.display.flip()