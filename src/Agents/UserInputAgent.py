from src.Agents.Agent import *
from src.Event.Event import Event

class UserInputAgent(Agent):
    def __init__(self):
        super().__init__()

    def handle_event(self, event_type: Event.EventType, data: dict):
        pass
