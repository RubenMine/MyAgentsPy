from src.Agents.Agent import *
from src.Event.Event import *
from src.Tasks.MailTasks import *


class EmailAgent(Agent):
    def __init__(self):
        super().__init__()

    def handle_event(self, event_type: Event.EventType, data: dict):
        #print(event_type)
        if event_type == SystemEvent.EventType.START:
            email_retrieval_task = EmailRetrievalTask(interval=100)
            email_retrieval_task.start()

        elif event_type == SystemEvent.EventType.STOP:
            #ADD SELF
            email_retrieval_task.stop()
            email_retrieval_task.join()

        elif event_type == MailEvent.EventType.NEW_EMAIL:
            task = ClassifyEmailTask(data)
            task.start()
            task.join()
        
        elif event_type == MailEvent.EventType.CLASSIFIED_EMAIL:
            task = FetchInfoEmailTask(data)
            task.start()
            task.join()
        