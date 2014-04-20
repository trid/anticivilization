from states.global_map_state import GlobalMapState
from application import application

__author__ = 'TriD'


state = GlobalMapState()
application.push_state(state)

while application.running:
    application.process()