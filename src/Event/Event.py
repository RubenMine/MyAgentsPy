from enum import Enum
import json 

class Event:
    class EventType(Enum):
        BASE = 0
        pass

    setting = False
    def __init__(self, type: EventType):
        self.e_type = type
        self.content = dict()
    
    def set(self):
        self.setting = True

    def is_set(self):
        return self.setting
    
    def get_content_to_json(self):
        return json.dumps(self.content, indent=4)
    

    
class SystemEvent(Event):
    class EventType(Enum):
        START = 0 
        STOP = 1

class MailEvent(Event):
    class EventType(Enum):
        NEW_EMAIL = 0
        CLASSIFIED_EMAIL = 1
        EXTRACT_INFO_EMAIL = 2
            
    def __init__(self, e_type): 
        super().__init__(e_type)
    
class InOutEvent(Event):
    class EventType(Enum):
        NEW_USER_IN = 0
            
    def __init__(self, e_type): 
        super().__init__(e_type)
        