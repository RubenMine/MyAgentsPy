from src.Tasks.Task import *
from src.Tools import GmailTool
from src.Event.Event import Event, MailEvent

class MailTask(Task):
    """
    class MailCategory(Enum):
        APPOINTMENT = 0
        WORK = 1
        INFORMATION = 2
        COMPLAINT = 3
        CONFIRMATION = 4
        FORWARDING = 5
        ADVERTISING = 6
        OTHER = 7
    """

    def __init__(self):
        self.gmail_tool = GmailTool()
        super().__init__()



import time
# Email Retrieval Task
class EmailRetrievalTask(MailTask):
    def __init__(self, interval: int = 60):
        self.interval = interval
        self.stop_event = Event(Event.EventType.BASE)
        super().__init__()

    def run(self):
        while not self.stop_event.is_set():
            unread_emails = self.gmail_tool.get_unread_emails()
            for email in unread_emails:
                me = MailEvent(MailEvent.EventType.NEW_EMAIL)
                me.content["mail_id"] = email.id
                me.content["plain"] = email.plain
                me.content["html"] = email.html
                self.event_system.send_event(me)

                #self.gmail_tool.mark_email_as_read(email)
            time.sleep(self.interval)

    def stop(self):
        self.stop_event.set()

# Email Process Task
class ClassifyEmailTask(MailTask):
    def __init__(self, me: MailEvent):
        self.gmail_tool = GmailTool()
        self.llm = LLMTool()

        self.me = me
        super().__init__()

    def run(self):
        content = self.me.content["plain"]  # Assuming plain text content
        html = self.me.content["html"]
        
        nme = MailEvent(MailEvent.EventType.CLASSIFIED_EMAIL)
        if content != None:
            nme.content["mail_id"] = self.me.content["mail_id"]
            nme.content["label"] = self.classify_email(content)
            nme.content["summary"] = self.summarize_email(content)
            self.event_system.send_event(nme)
            #self.gmail_tool.move_email_to_folder(email, category)
        else:
            nme.content["mail_id"] = self.me.content["mail_id"]
            nme.content["label"] = self.classify_email(html)
            nme.content["summary"] = self.summarize_email(html)
            self.event_system.send_event(nme)

    def classify_email(self, content: str) -> str:
        role = "RISPONDI SOLO CON 1 PAROLA\
                Descrizione del compito: Riceverai email contenenti vari messaggi. Il tuo compito è leggere ogni email e classificarla in base al contenuto. Devi rispondere indicando solo una parola che rappresenta meglio la categoria o il tipo di email ricevuta. La parola deve essere contenuta nella seguente lista.\
                Categorie possibili:\
                    [LAVORO, APPUNTAMENTO, INFORMAZIONI, ORDINE, RECLAMO, CONFERMA, INOLTRO, PUBBLICITA, ALTRO]\
                Spiegazione Categorie:\
                    Lavoro: se l'email contiene comunicazioni di Lavoro o riguardo a Stage e opportunità.\
                    Appuntamento: Se l'email contiene una richiesta di organizzare o confermare un incontro. in genere se possiede una data e altre informazioni riconducibili\
                    Informazioni: Se l'email chiede dettagli o chiarimenti su un argomento specifico.\
                    Ordine: Se l'email riguarda un ordine, spedizione o aggiornamento di acquisto.\
                    Reclamo: Se l'email contiene una lamentela o una richiesta di assistenza.\
                    Conferma: Se l'email riguarda una conferma di ricezione o conferma di un'azione eseguita.\
                    Inoltro: Se l'email richiede di essere inviata a un altro reparto o collega.\
                    Pubblicità: Se l'email contiene una proposta commerciale o un messaggio promozionale.\
                    Altro: Se l'email non rientra nelle categorie sopra elencate.\
                Formato di risposta:\
                    Rispondi con solo la parola che rappresenta la categoria dell'email\n"

        classe = self.llm.respond(role, content)
        return classe
    
    def summarize_email(self, content: str) -> str:
        role = "Descrizione del compito: Riceverai varie Email. Il tuo compito è leggere ogni Email e riassumerla tenendo tutte le informazioni necessarie.\
                Formato di risposta:\
                    Devi rispondere SOLTANTO con il riassunto tenendo tutte le informazioni necessarie\n"
        
        summ = self.llm.respond(role, content)
        return summ


import json
class FetchInfoEmailTask(MailTask):
    def __init__(self, me: MailEvent):
        self.gmail_tool = GmailTool()
        self.llm = LLMTool()

        self.me = me
        super().__init__()

    def run(self):
        category = self.me.content["label"]  # Assuming plain text content
        if ("APPUNTAMENTO" in category.upper().split()):
            nme = MailEvent(MailEvent.EventType.EXTRACT_INFO_EMAIL)

            jsontxt = self.fetch_appuntamento(self.me.content["summary"])

            try:
                nme.content = json.loads(jsontxt)
            except:
                nme.content["JSON"] = jsontxt

            self.event_system.send_event(nme)


    def fetch_appuntamento(self, content: str) -> str:
        role = "Descrizione del compito: Riceverai vari messaggi. Il tuo compito è leggere ogni messaggio e formattare in json le informazioni necessarie.\
                Formato di risposta:\
                    Devi rispondere SOLTANTO con il testo in json e compilando i seguenti campi. Se non specificato inserire None\
                Campi da compilare:\
                    Descrizione:\
                    Luogo:\
                    Data:\
                    Ora:\n"
        
        info = self.llm.respond(role, content)
        return info
         