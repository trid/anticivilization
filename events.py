import pygame

__author__ = 'TriD'


class EventProcessor:
    def __init__(self, data, uis, display):
        self.data = data
        self.uis = uis
        self.display = display

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.data.done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.data.buttons_active = True
                    buttons_pos = event.pos
                    self.uis.setup_buttons(*buttons_pos)
                    if self.data.game_map[(buttons_pos[0] + self.data.dx - self.data.dx % 32) / 32][(buttons_pos[1] + self.data.dy - self.data.dy % 32) / 32].resource:
                        self.uis.set_resource_click_buttons()
                        self.data.exp_pos = ((buttons_pos[0] + self.data.dx - self.data.dx % 32) / 32, (buttons_pos[1] + self.data.dy - self.data.dy % 32) / 32)
                    else:
                        self.uis.set_grass_click()
                    building = None
                if event.button == 1:
                    if self.data.buttons_active:
                        self.data.buttons_active = False
                        self.uis.process_buttons(*event.pos)
                    elif self.uis.building:
                        self.data.build(*event.pos)
                    if self.data.drag:
                        self.data.drag = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.data.next_turn()
            if event.type == pygame.MOUSEMOTION:
                self.display.mouse_x, self.display.mouse_y = event.pos
                if self.data.drag:
                    #And here we move the map on the screen
                    mouse_pos_x, mouse_pos_y = event.pos
                    self.data.dx = self.data.old_dx + (mouse_pos_x - self.data.mouse_drag_x)
                    self.data.dy = self.data.old_dy + (mouse_pos_y - self.data.mouse_drag_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #Here we start drag the map
                    self.data.drag = True
                    self.data.mouse_drag_x, self.data.mouse_drag_y = event.pos
                    self.data.old_dx = self.data.dx
                    self.data.old_dy = self.data.dy