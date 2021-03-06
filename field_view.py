from pygame.rect import Rect
from pygame.surface import Surface
from sprite_manager import SpriteManager

__author__ = 'TriD'


class FieldView:
    def __init__(self, game_data):
        self.game_data = game_data
        self.mouse_x, self.mouse_y = 0, 0
        self.sm = SpriteManager()
        self.selected_tile_surface_no_building = Surface((32, 32))
        self.selected_tile_surface_no_building.fill(0xb7f315)
        self.selected_tile_surface_no_building.set_alpha(124)
        self.selected_tile_surface_destroy = Surface((32, 32))
        self.selected_tile_surface_destroy.fill(0xff0000)
        self.selected_tile_surface_destroy.set_alpha(124)
        self.selected_tile_surface = self.selected_tile_surface_no_building
        self.road_data = (1, 1, 0, 10, 0, 9, 0, 4, 1, 1, 8, 6, 7, 5, 3, 2)

    def draw_sprite(self, screen, x, y, sprite):
        if x + 32 <= 600:
            screen.blit(sprite, [x, y])
        elif 632 > x + 32 > 600:
            screen.blit(sprite, [x, y], Rect(0, 0, 600 - x, sprite.get_height()))

    def draw_field(self, screen):
        for x in range(0, 20):
            for y in range(0, 20):
                # New, better rendering that draws part of map that is currently on screen
                mx = x + self.game_data.dx / 32
                my = y + self.game_data.dy / 32
                sx = x * 32 - self.game_data.dx % 32
                sy = y * 32 - self.game_data.dy % 32
                self.draw_sprite(screen, sx, sy, self.sm.sprites[self.game_data.game_map[mx][my].ground])
                if self.game_data.game_map[mx][my].resource:
                    self.draw_sprite(screen, sx, sy, self.sm.sprites[self.game_data.game_map[mx][my].resource])
                if self.game_data.game_map[mx][my].building == 'center':
                    self.draw_sprite(screen, sx, sy - 64, self.sm.sprites['center'])
                elif self.game_data.game_map[mx][my].building == 'road':
                    self.draw_road_tile(self.game_data.game_map, mx, my, screen)
                elif self.game_data.game_map[mx][my].building:
                    self.draw_sprite(screen, sx, sy, self.sm.sprites[self.game_data.game_map[mx][my].building])
        for expedition in self.game_data.expeditions:
            self.draw_sprite(screen, expedition.x * 32 - self.game_data.dx, expedition.y * 32 - 28 - self.game_data.dy, self.sm.sprites['human'])
        for monster in self.game_data.monsters:
            self.draw_sprite(screen, monster.x * 32 - self.game_data.dx, monster.y * 32 - self.game_data.dy, self.sm.sprites['monster'])

        lighted_x = ((self.mouse_x + self.game_data.dx) / 32) * 32 - self.game_data.dx
        lighted_y = ((self.mouse_y + self.game_data.dy) / 32) * 32 - self.game_data.dy
        self.set_selecter_surface()
        #self.draw_sprite(screen, lighted_x, lighted_y, self.selected_tile_surface)
        screen.blit(self.selected_tile_surface, [lighted_x, lighted_y], Rect(0, 0, 32, self.selected_tile_surface.get_height()))

    def draw_road_tile(self, game_map, position_x, position_y, screen):
        """
        Road drawing as it have to be
        """
        tile_num = 0
        if game_map[position_x][position_y - 1].building == 'road':
            tile_num += 1
        if game_map[position_x - 1][position_y].building == 'road':
            tile_num += 2
        if game_map[position_x + 1][position_y].building == 'road':
            tile_num += 4
        if game_map[position_x][position_y + 1].building == 'road':
            tile_num += 8

        sx = position_x * 32 - self.game_data.dx
        sy = position_y * 32 - self.game_data.dy
        self.blit_road_tile(sx, sy, screen, self.road_data[tile_num])

    #TODO: merge two blitting methods
    def blit_road_tile(self, x, y, screen, item):
        sprite = self.sm.sprites['road']
        if x + 32 <= 600:
            screen.blit(sprite, [x, y], Rect(item * 32, 0, 32, sprite.get_height()))
        elif 632 > x + 32 > 600:
            screen.blit(sprite, [x, y], Rect(item * 32, 0, 600 - x, sprite.get_height()))

    def set_selecter_surface(self):
        if self.game_data.uis.building and self.game_data.uis.building != 'destruct':
            surface = SpriteManager().sprites[self.game_data.uis.building].copy()
            self.selected_tile_surface = surface
        elif self.game_data.uis.building == 'destruct':
            self.selected_tile_surface = self.selected_tile_surface_destroy
        else:
            self.selected_tile_surface = self.selected_tile_surface_no_building