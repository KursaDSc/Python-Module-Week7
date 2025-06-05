from PyQt6.QtCore import QObject, pyqtSignal

class SheetsLoaderWorker(QObject):
    finished = pyqtSignal(list)

    def __init__(self, sheet_service, sheet_id, range_name):
        super().__init__()
        self.sheet_service = sheet_service
        self.sheet_id = sheet_id
        self.range_name = range_name

    def run(self):
        events_raw = self.sheet_service.list_events(max_results=20)
        self.finished.emit(events_raw)