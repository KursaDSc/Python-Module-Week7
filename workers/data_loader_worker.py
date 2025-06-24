from PyQt6.QtCore import QObject, pyqtSignal
from services.auth import authenticate
from services.db import get_data

class DatabaseAuthWorker(QObject):
    finished = pyqtSignal(object)

    def __init__(self, query, params, password_input):
        super().__init__()
        self.query = query
        self.params = params
        self.password_input = password_input

    def run(self):
        row = get_data(self.query, self.params)  # ('john', 'hashed_pass', 'admin') gibi bir tuple
        user = authenticate(self.params[0], self.password_input, row)
        self.finished.emit(user)