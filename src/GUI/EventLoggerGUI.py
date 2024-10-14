import tkinter as tk
from tkinter import scrolledtext

from src.Event.EventSystem import event_details_storage  # Importiamo il dizionario globale


class EventLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Logger")

        # Event list box (lista con i riassunti brevi)
        self.event_listbox = tk.Listbox(root, width=50, height=20)
        self.event_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.event_listbox.bind("<<ListboxSelect>>", self.on_event_select)

        # Event details box (dettagli completi, scrollable text widget)
        self.event_details = scrolledtext.ScrolledText(root, width=60, height=20)
        self.event_details.grid(row=0, column=1, padx=10, pady=10)

        # Start the periodic update of the event list
        self.update_event_list()

    def update_event_list(self):
        """Fetch the logged events from the log file and update the listbox."""
        try:
            with open("events.log", "r") as file:
                log_lines = file.readlines()

            # Clear the listbox before updating
            self.event_listbox.delete(0, tk.END)

            # Insert new lines in the listbox
            for idx, line in enumerate(log_lines):
                self.event_listbox.insert(tk.END, f"{line.strip()}")

        except FileNotFoundError:
            self.event_listbox.insert(tk.END, "Log file not found.")

        # Schedule the next update in 1 second
        self.root.after(1000, self.update_event_list)

    def on_event_select(self, event):
        """Display details of the selected event."""
        selection = self.event_listbox.curselection()
        if selection:
            index = selection[0]  # Otteniamo l'ID dell'evento selezionato
            #event_id = int(self.event_listbox.get(index).split(":")[0])  # Estrarre l'ID
            # Recupera i dettagli dall'evento selezionato dal dizionario in memoria
            event_details = event_details_storage.get(index, "No details available for this event.")
            self.event_details.delete(1.0, tk.END)
            self.event_details.insert(tk.END, str(event_details))  # Mostra i dettagli completi

# Funzione per avviare il logger GUI
def start_logger():
    root = tk.Tk()
    gui = EventLoggerGUI(root)
    root.mainloop()

