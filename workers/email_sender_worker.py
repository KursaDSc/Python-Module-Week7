from PyQt6.QtCore import QObject, pyqtSignal

class EmailSenderWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, personalized_emails, send_email_func):
        super().__init__()
        self.personalized_emails = personalized_emails  # [(email, subject, body), ...]
        self.send_email_func = send_email_func

    def run(self):
        for email, subject, body in self.personalized_emails:
            self.send_email_func(email, subject, body)
        self.finished.emit()