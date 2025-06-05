from PyQt6.QtCore import QObject, pyqtSignal

class EmailSenderWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, emails, subject, body, send_email_func):
        super().__init__()
        self.emails = emails
        self.subject = subject
        self.body = body
        self.send_email_func = send_email_func

    def run(self):
        for email in self.emails:
            self.send_email_func(email, self.subject, self.body)
        self.finished.emit()