from application import application
from states.start_menu_state import StartMenuState

__author__ = 'TriD'


state = StartMenuState()
application.push_state(state)

while application.running:
    application.process()