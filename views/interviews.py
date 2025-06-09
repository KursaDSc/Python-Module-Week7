import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS, SheetName
from PyQt6.QtWidgets import QHeaderView, QAbstractScrollArea, QSizeGrip


class InterviewsWindow(QtWidgets.QMainWindow):
    def __init__(self, is_admin=False, previous_window=None):
        super().__init__()
        ui_folder = os.path.join(os.path.dirname(__file__), "ui")
        ui_path = os.path.join(ui_folder, "interviews.ui")
        uic.loadUi("ui/interviews.ui", self)
        # ------------------------------------------------------------

        self.is_admin = is_admin
        self.previous_window = previous_window

        # Pencereyi çerçevesiz + transparan yapmak için
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.sheet_service = GoogleSheetsService()
        self.interviews_config = GOOGLE_SHEETS[SheetName.INTERVIEW]


        # Fareyle sürüklemek için kullanılacak değişkenler
        self.drag_position = QPoint()
        self.resize_grip = QSizeGrip(self)
        self.resize_grip.setStyleSheet("background: transparent;")
        self.resize_grip.resize(16, 16)

        # ------------------------------------------------------------
        # 2) findChild(...) ile UI elemanlarını alırken, mutlaka
        #    .ui içindeki objectName ile aynısı olsun:
        # ------------------------------------------------------------
        self.search_edit    = self.findChild(QtWidgets.QLineEdit,     "searchBoxLine")
        self.search_button  = self.findChild(QtWidgets.QPushButton,   "searchButton")
        self.back_button    = self.findChild(QtWidgets.QPushButton,   "returnButton")
        self.exit_button    = self.findChild(QtWidgets.QPushButton,   "exitButton")
        self.interview_table = self.findChild(QtWidgets.QTableWidget,  "tabloWidget")
        self.sent_button     = self.findChild(QtWidgets.QPushButton, "projectButton")
        self.received_button = self.findChild(QtWidgets.QPushButton, "projectNotButton")


        # Eğer yukarıdakilerden ANY biri None döndüyse, objectName'ler
        # .ui dosyasındakiyle tam eşleşmiyordur; hemen uyarı fırlatalım:
        if None in [
            self.search_edit,
            self.search_button,
            self.back_button,
            self.exit_button,
            self.interview_table,
            self.sent_button,
            self.received_button
        ]:
            raise RuntimeError(
                "Bazı UI öğeleri bulunamadı! "
                "Lütfen interviews.ui içindeki objectName değerlerini ve "
                "loadUi yolu doğruluğunu kontrol edin."
            )
        # ------------------------------------------------------------

        # Tablo başlık boyutlandırma, kaydırma vb. ayarları
        header = self.interview_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.interview_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.interview_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.interview_table.verticalHeader().setVisible(False)

        # Event (sinyal-slot) bağlamaları
        self.search_button.clicked.connect(self.search_data)
        self.search_edit.returnPressed.connect(self.search_data)
        self.back_button.clicked.connect(self.go_back)
        self.exit_button.clicked.connect(self.close)

        self.sent_button.clicked.connect(self.filter_sent_projects)
        self.received_button.clicked.connect(self.filter_received_projects)


        # Google Sheets servisini başlat, veriyi yükle
        self.sheet_service = GoogleSheetsService()
        self.sheet_config = GOOGLE_SHEETS[SheetName.INTERVIEW]
        self.load_data()
        

    def load_data(self):
        data = self.sheet_service.read_data(
            sheet_id=self.sheet_config["sheet_id"],
            range_name=self.sheet_config["ranges"]
        )
        self.full_data = data
        self.populate_table(data)

    def populate_table(self, data: list):
        self.interview_table.setRowCount(0)

        if not data:
            self.interview_table.setColumnCount(0)
            return

        headers = data[0]
        self.interview_table.setColumnCount(len(headers))
        self.interview_table.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(data[1:]):
            self.interview_table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.interview_table.setItem(row_idx, col_idx, item)

    # def search_data(self):
    #     keyword = self.search_edit.text().lower()
    #     headers = self.full_data[0]
    #     name_column_index = 0  # isim ve soyisimin bulundugu indeks
    #     filtered = [
    #         row for row in self.full_data[1:]
    #         if name_column_index < len(row) and row[name_column_index].lower().startswith(keyword)
    #     ]
    #     self.populate_table([headers] + filtered if filtered else [headers])


    def search_data(self):
        keyword = self.search_edit.text().lower().strip()
        headers = self.full_data[0]
        name_column_index = 0  # isim indeks
        print("Sütun başlıkları:", headers)  # DEBUG

        if not keyword:
            self.populate_table(self.full_data)
            return

        filtered = []
        for row in self.full_data[1:]:
            if name_column_index < len(row):
                name = row[name_column_index]
                if isinstance(name, str) and name.lower().startswith(keyword):
                    filtered.append(row)
        self.populate_table([headers] + filtered if filtered else [headers])
    
    def go_back(self):
        if self.is_admin:
            from views.preferences_admin import AdminPreferencesWindow
            self.window = AdminPreferencesWindow()
        else:
            from views.preferences import UserPreferencesWindow
            self.window = UserPreferencesWindow()
        self.window.show()
        self.close()

    # Fare ile pencereyi sürüklemek için:
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def filter_sent_projects(self):
        if not hasattr(self, "full_data") or not self.full_data:
            return

        headers = self.full_data[0]
        data = self.full_data[1:]
        try:
            idx = headers.index("Proje gonderilis tarihi")
        except ValueError:
            print("Sütun bulunamadı: Proje gonderilis tarihi")
            return

        filtered = [row for row in data if idx < len(row) and row[idx].strip()]
        self.populate_table([headers] + filtered if filtered else [headers])

    def filter_received_projects(self):
        if not hasattr(self, "full_data") or not self.full_data:
            return

        headers = self.full_data[0]
        data = self.full_data[1:]
        try:
            idx = headers.index("Projenin gelis tarihi")
        except ValueError:
            print("Sütun bulunamadı: Projenin gelis tarihi")
            return

        filtered = [row for row in data if idx < len(row) and row[idx].strip()]
        self.populate_table([headers] + filtered if filtered else [headers])
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterviewsWindow()
    window.show()
    sys.exit(app.exec())

