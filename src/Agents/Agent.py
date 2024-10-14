from abc import ABC, abstractmethod
from src.Tools import LLMTool

from src.Event.EventSystem import EventSystem as ES
from src.Event.Event import *
from src.Tasks.Task import * 

class Agent(ABC):
    def __init__(self):
        self.event_system = ES()
    
    @abstractmethod
    def handle_event(self, evento):
        pass


class AIAgent(Agent):
    def __init__(self, name, api_key):
        self.llm = LLMTool(api_key)
        self.role = ""

        super().__init__(name)
        #test = "sk-awjLSL7m34SJnv4cGMeE5pL-RKWk_Pw1giInch2Ka7T3BlbkFJHNTDk20KT_3T0K9hSI4bzGeZFaAkp0xG9aeJJe3A0A"

    def get_response(self, system_role, user_content):
        pass
    
    def handle_event(self, evento):
        #print(evento.content)
        pass


