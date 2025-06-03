import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS, SheetName

class MentorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mentor.ui", self)

        self.sheet_service = GoogleSheetsService()
        self.mentor_config = GOOGLE_SHEETS[SheetName.MENTOR]


        # Arayüz öğeleri
        self.search_button.clicked.connect(self.search_data)
        self.search_edit.returnPressed.connect(self.search_data)
        self.search_edit = self.findChild(QtWidgets.QLineEdit, "search_edit")
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.all_applications_button = self.findChild(QtWidgets.QPushButton, "all_applications_button")
        self.decision_combobox = self.findChild(QtWidgets.QComboBox, "decision_combobox")
        self.applications_table = self.findChild(QtWidgets.QTableWidget, "applications_table")
        self.applications_table.verticalHeader().setVisible(False)

        self.exit_button = self.findChild(QtWidgets.QPushButton, "exit_button")
        self.back_button = self.findChild(QtWidgets.QPushButton, "back_button")

        # Bağlantılar
        self.search_button.clicked.connect(self.search_data)
        self.all_applications_button.clicked.connect(self.load_all_conversations)
        self.exit_button.clicked.connect(self.close)
        self.decision_combobox.currentTextChanged.connect(self.handle_decision_change)

        # Pencereyi büyüt
        self.resize(1000, 700)
        self.load_all_conversations()

    def handle_decision_change(self, text):
        print(f"Seçilen karar: {text}")
        self.load_all_conversations()

    def load_all_conversations(self):
        data = self.sheet_service.read_data(
            sheet_id=self.mentor_config["sheet_id"],
            range_name=self.mentor_config["ranges"]
        )
        self.full_data = data
        self.populate_table(data)

    def search_data(self):
        keyword = self.search_edit.text().lower()
        all_data = self.sheet_service.read_data(
            sheet_id=self.mentor_config["sheet_id"],
            range_name=self.mentor_config["ranges"]
        )

        self.full_data = all_data

        if len(all_data) < 1:
            return

        headers = all_data[0]
        rows = all_data[1:]

        filtered = [row for row in rows if keyword in str(row).lower()]

        if filtered:
            self.populate_table([headers] + filtered)
        else:
            self.populate_table([headers])


    def populate_table(self, data: list):
        self.applications_table.setRowCount(0)

        if not data:
            self.applications_table.setColumnCount(0)
            return

        # Her durumda ilk satır başlıklar olmalı
        headers = data[0]
        self.applications_table.setColumnCount(len(headers))
        self.applications_table.setHorizontalHeaderLabels(headers)

        # Eğer sadece başlık varsa (veri yoksa), tabloyu boş göster
        if len(data) == 1:
            return

        # Diğer satırları doldur
        for row_index, row_data in enumerate(data[1:]):
            self.applications_table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.applications_table.setItem(row_index, col_index, item)

        self.applications_table.resizeColumnsToContents()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MentorWindow()
    window.show()
    sys.exit(app.exec())
