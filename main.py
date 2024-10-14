import threading
from src.Event.EventSystem import EventSystem as ES
from src.GUI.EventLoggerGUI import start_logger

from src.Agents.Agent import *
from src.Agents.EmailAgent import EmailAgent
from src.Agents.UserInputAgent import UserInputAgent

import time

# Main execution
if __name__ == "__main__":
    logger_thread = threading.Thread(target=start_logger, daemon=True)
    logger_thread.start()
    
    # Initialize agents
    email_classifier_agent = EmailAgent()
    ES().subscribe(email_classifier_agent, [SystemEvent, MailEvent])

    user_input_agent = UserInputAgent()
    ES().subscribe(user_input_agent, [SystemEvent, InOutEvent])


    ES().send_event(SystemEvent(SystemEvent.EventType.START))
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        ES().send_event(SystemEvent(SystemEvent.EventType.STOP))