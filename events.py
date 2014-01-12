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
                if self.uis.dialog:
                    if event.button == 1:
                        self.uis.process_clicks(*event.pos)
                        continue
                elif event.button == 3:
                    if event.pos[0] > 600:
                        continue
                    self.data.popup_active = True
                    buttons_pos = event.pos
                    if self.data.game_map[(buttons_pos[0] + self.data.dx) / 32][(buttons_pos[1] + self.data.dy) / 32].resource:
                        self.uis.set_resource_click_buttons()
                        self.data.exp_pos = ((buttons_pos[0] + self.data.dx) / 32, (buttons_pos[1] + self.data.dy) / 32)
                    else:
                        self.uis.set_grass_click()
                    self.uis.setup_buttons(*buttons_pos)
                    building = None
                if event.button == 1:
                    if self.data.popup_active:
                        self.data.popup_active = False
                        self.uis.process_popup(*event.pos)
                        continue
                    elif self.uis.process_clicks(*event.pos):
                        pass
                    elif self.uis.building and event.pos[0] < 600:
                        self.data.build(*event.pos)
                    if self.data.drag:
                        self.data.drag = False
            if event.type == pygame.KEYUP:
                if not self.uis.dialog:
                    if event.key == pygame.K_RETURN:
                        self.data.next_turn()
                else:
                    if event.key == pygame.K_RETURN:
                        if self.uis.dialog.enter_btn:
                            self.uis.dialog.enter_btn.run_callback()
                    elif event.key == pygame.K_ESCAPE:
                        if self.uis.dialog.esc_btn:
                            self.uis.dialog.esc_btn.run_callback()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.data.scroll_spd_y = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.data.scroll_spd_x = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.data.scroll_spd_y = -5
                if event.key == pygame.K_LEFT:
                    self.data.scroll_spd_x = -5
                if event.key == pygame.K_DOWN:
                    self.data.scroll_spd_y = 5
                if event.key == pygame.K_RIGHT:
                    self.data.scroll_spd_x = 5
            if event.type == pygame.MOUSEMOTION:
                self.display.mouse_x, self.display.mouse_y = event.pos
                if self.data.drag:
                    #And here we move the map on the screen
                    mouse_pos_x, mouse_pos_y = event.pos
                    self.data.dx = self.data.old_dx + (mouse_pos_x - self.data.mouse_drag_x)
                    self.data.dy = self.data.old_dy + (mouse_pos_y - self.data.mouse_drag_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.data.popup_active and event.pos[0] < 600 and not self.uis.dialog:
                    #Here we start drag the map
                    self.data.drag = True
                    self.data.mouse_drag_x, self.data.mouse_drag_y = event.pos
                    self.data.old_dx = self.data.dx
                    self.data.old_dy = self.data.dy