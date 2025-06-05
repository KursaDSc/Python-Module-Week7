from PyQt6.QtCore import QObject, pyqtSignal

class DataLoaderWorker(QObject):
    finished = pyqtSignal(list)

    def __init__(self, sheet_service, sheet_id, range_name):
        super().__init__()
        self.sheet_service = sheet_service
        self.sheet_id = sheet_id
        self.range_name = range_name

    def run(self):
        users = self.sheet_service.read_data(self.sheet_id, self.range_name)
        if users:
            self.finished.emit(users[1:])  # Skip header
        else:
            self.finished.emit([])