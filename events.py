import pygame
from application import application

__author__ = 'TriD'


class EventProcessor:
    def __init__(self, data, uis, display):
        self.data = data
        self.uis = uis
        self.display = display
        self.mouse_listeners = []
        self.keyboard_listeners = []

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                application.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for listener in self.mouse_listeners:
                    listener.mouse_event(event)
                if event.button == 3:
                    if event.pos[0] > 600:
                        continue
                    self.data.popup_active = True
                    buttons_pos = event.pos
                    tile = self.data.game_map[(buttons_pos[0] + self.data.dx) / 32][(buttons_pos[1] + self.data.dy) / 32]
                    self.uis.show_map_popup(buttons_pos[0], buttons_pos[1], tile)
                    self.uis.building = None
                    continue
                if event.button == 1:
                    if self.uis.building and event.pos[0] < 600:
                        self.data.build(*event.pos)
                    if self.data.drag:
                        self.data.drag = False
                if self.uis.process_clicks(event.pos[0], event.pos[1], event.button):
                    continue
            elif event.type == pygame.KEYUP:
                for listener in self.keyboard_listeners:
                    listener.keyboard_up(event)
                if not self.uis.dialog:
                    if event.key == pygame.K_RETURN:
                        self.data.next_turn()
                    if event.key == pygame.K_ESCAPE:
                        self.uis.dialog = self.uis.main_menu
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
                for listener in self.keyboard_listeners:
                    listener.keyboard_down(event)
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
                else:
                    if event.pos[0] < 10:
                        self.data.scroll_spd_x = -5
                    elif 590 < event.pos[0] < 600:
                        self.data.scroll_spd_x = 5
                    else:
                        self.data.scroll_spd_x = 0
                    if event.pos[1] < 10:
                        self.data.scroll_spd_y = -5
                    elif event.pos[1] > 590:
                        self.data.scroll_spd_y = 5
                    else:
                        self.data.scroll_spd_y = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and event.pos[0] < 600 and not self.uis.dialog:
                    #Here we start drag the map
                    self.data.drag = True
                    self.data.mouse_drag_x, self.data.mouse_drag_y = event.pos
                    self.data.old_dx = self.data.dx
                    self.data.old_dy = self.data.dy