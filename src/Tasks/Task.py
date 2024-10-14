from src.Tools import LLMTool

from src.Event.Event import Event
from src.Event.EventSystem import EventSystem as ES

from enum import Enum
from threading import Thread

# Agent
class Task(Thread):
    def __init__(self):
        self.event_system = ES()
        super().__init__()



