import logging

# Funzione per aggiungere i dati extra nei log
class EventLogFilter(logging.Filter):
    def filter(self, record):
        # Se il campo extra non esiste, lo creiamo vuoto
        if not hasattr(record, 'event_data'):
            record.event_data = 'No event data'
        return 'Event:' in record.getMessage()
    

open("events.log", "w").close()

# Configura un logger separato solo per gli eventi, senza ereditare dal logger di root
event_logger = logging.getLogger('event_logger')
event_logger.setLevel(logging.INFO)
event_logger.propagate = False  # Disabilita ereditarietà dal logger di root
event_logger.addFilter(EventLogFilter())  # Aggiungi il filtro personalizzato per i dati extra

# Configura FileHandler per il logger separato
file_handler = logging.FileHandler("events.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
event_logger.addHandler(file_handler)