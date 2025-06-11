import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS, SheetName

class MentorWindow(QtWidgets.QMainWindow):
    def __init__(self, is_admin=False, previous_window=None):
        super().__init__()
        uic.loadUi("ui/mentor.ui", self)
        self.is_admin = is_admin
        self.previous_window = previous_window

        self.sheet_service = GoogleSheetsService()
        self.mentor_config = GOOGLE_SHEETS[SheetName.MENTOR]

        #Çeviri
        self.header_translation = {
            "Gorusme tarihi": "Meeting Date",
            "Mentinin adi soyadi": "Mentee Name",
            "Mentorün adı-soyadı": "Mentor Name",
            "Katılımcı IT sektörü hakkında bilgi sahibi mi?": "IT Knowledge",
            "VIT projesinin tamamına katılması uygun olur": "Decision",
            "Katılımcı hakkında ne düşünüyorsunuz": "Feedback",
            "Katilimcinin yogunluk durumu": "Availability",
            "Katilimci hakkinda yorumlar": "Comment"
        }

        # Pencere ayarları
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.drag_position = QPoint()

        # Arayüz öğeleri
        self.search_edit = self.findChild(QtWidgets.QLineEdit, "search_edit")
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.all_applications_button = self.findChild(QtWidgets.QPushButton, "all_applications_button")
        self.decision_combobox = self.findChild(QtWidgets.QComboBox, "decision_combobox")
        self.applications_table = self.findChild(QtWidgets.QTableWidget, "applications_table")
        self.applications_table.verticalHeader().setVisible(False)

        self.exit_button = self.findChild(QtWidgets.QPushButton, "exit_button")
        self.back_button = self.findChild(QtWidgets.QPushButton, "back_button")
        self.preferences_button = self.findChild(QtWidgets.QPushButton, "preferences_button")

        # Bağlantılar
        self.search_button.clicked.connect(self.search_data)
        self.search_edit.returnPressed.connect(self.search_data)
        self.all_applications_button.clicked.connect(self.load_all_conversations)
        self.exit_button.clicked.connect(self.close)
        self.back_button.clicked.connect(self.handle_back)
        self.decision_combobox.currentTextChanged.connect(self.filter_by_decision)

        self.load_all_conversations()
        self.load_decision_combobox()

    def load_all_conversations(self):
        data = self.sheet_service.read_data(
            sheet_id=self.mentor_config["sheet_id"],
            range_name=self.mentor_config["ranges"]
        )
        self.full_data = data
        self.populate_table(data)

    def load_decision_combobox(self):
        decision_config = GOOGLE_SHEETS[SheetName.DECISION]
        data = self.sheet_service.read_data(
            sheet_id=decision_config["sheet_id"],
            range_name=decision_config["ranges"]
        )
        if data and len(data) > 1:
            values = [row[0] for row in data[1:] if row and row[0]]
            self.decision_combobox.clear()
            self.decision_combobox.addItem("Choose Filter...")
            self.decision_combobox.addItems(sorted(set(values)))

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

        headers = data[0]
        self.applications_table.setColumnCount(len(headers))
        translated_headers = [self.header_translation.get(h, h) for h in headers]
        self.applications_table.setHorizontalHeaderLabels(translated_headers)

        if len(data) == 1:
            return

        for row_index, row_data in enumerate(data[1:]):
            self.applications_table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                tooltip_html = f'<div style="max-width:300px; white-space:normal;">{str(value)}</div>'
                item.setToolTip(tooltip_html)
                self.applications_table.setItem(row_index, col_index, item)

        total_width = sum(self.applications_table.columnWidth(i) for i in range(self.applications_table.columnCount()))
        self.resize(total_width + 50, self.height())

    def filter_by_decision(self, decision):
        if decision == "Choose Filter..." or not decision.strip():
            self.search_edit.clear()
            self.search_data()
            return

        keyword = decision.lower()
        all_data = self.full_data
        if not all_data or len(all_data) < 2:
            return

        headers = all_data[0]
        rows = all_data[1:]
        filtered = [row for row in rows if keyword in str(row).lower()]
        if filtered:
            self.populate_table([headers] + filtered)
        else:
            self.populate_table([headers])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def handle_back(self):
        print("🔙 Geri butonuna basıldı")
        if self.previous_window:
            self.previous_window.show()
            self.previous_window.raise_()
            self.previous_window.activateWindow()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QToolTip { background-color: #fff8dc; color: #222; border: 1px solid #a9a9a9; }")
    window = MentorWindow()
    window.show()
    sys.exit(app.exec())
