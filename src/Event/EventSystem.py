import src.Event.Event as Event
from src.Logger.logger import event_logger

# Memoria per i dettagli degli eventi
event_details_storage = {}

class EventSystem:
    _instance = None
    def __new__(cls):
        """Ensure that only one instance of EventSystem is created."""
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._instance._subscribers = {}  # Dictionary to hold event subscribers
        return cls._instance

    def subscribe(self, agent, event_categories):
        """Subscribe an agent to specific event types."""
        for e_type in event_categories:
            if e_type not in self._subscribers:
                self._subscribers[e_type] = []
            self._subscribers[e_type].append(agent)

    def unsubscribe(self, agent):
        """Unsubscribe an agent from all events."""
        for e_type in self._subscribers:
            if agent in self._subscribers[e_type]:
                self._subscribers[e_type].remove(agent)

    def send_event(self, event):
        """Send an event to all subscribed agents."""
        event_id = len(event_details_storage)  # Usiamo l'indice del log come chiave
        event_details_storage[event_id] = event.get_content_to_json()  # Salva i dettagli dell'evento in memoria
        log_entry = f"Event: {type(event).__name__} -> {event.e_type.name}"
        event_logger.info(log_entry, extra={'event_data': event.get_content_to_json()})

        if type(event) in self._subscribers:
            for agent in self._subscribers[type(event)]:
                agent.handle_event(event.e_type, event)

    def get_subscribers(self):
        """Return the current subscribers for testing or inspection."""
        return self._subscribers

    def get_event_log(self):
        """Return the current event log."""
        return self._event_log


