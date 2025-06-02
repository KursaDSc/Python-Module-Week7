import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS, SheetName

class MentorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mentor.ui", self)

        self.sheet_service = GoogleSheetsService()
        self.mentor_config = GOOGLE_SHEETS[SheetName.MENTOR]
        
        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Buton bağlantıları
        self.allConversationsButton.clicked.connect(self.load_all_conversations)
        self.searchButton.clicked.connect(self.search_data)
        


    def load_all_conversations(self):
        data = self.sheet_service.read_data(
            sheet_id=self.mentor_config["sheet_id"],
            range_name=self.mentor_config["ranges"]
        )
        self.populate_table(data)

    def search_data(self):
        keyword = self.searchInput.text().lower()
        all_data = self.sheet_service.read_data(
            sheet_id=self.mentor_config["sheet_id"],
            range_name=self.mentor_config["ranges"]
        )
        filtered = [row for row in all_data if keyword in str(row).lower()]
        self.populate_table(filtered)

    def populate_table(self, data: list):
        self.tableWidget.setRowCount(0)
        if not data:
            self.tableWidget.setColumnCount(0)
            return

        headers = data[0]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data[1:]):
            self.tableWidget.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))
