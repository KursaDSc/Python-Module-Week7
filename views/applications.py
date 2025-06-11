import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS, SheetName

class ApplicationsWindow(QtWidgets.QMainWindow):
    """
    Main window for viewing and filtering application data from Google Sheets.
    Supports:
    - Full data view
    - Mentor assignment filtering
    - Duplicate entry detection
    - Name-based search
    - Comparison with external VIT lists
    """
    def __init__(self, is_admin=False, previous_window=None):
        super().__init__()
        uic.loadUi("ui/applications.ui", self)
        self.previous_window = previous_window

        self.is_admin = is_admin

        # Initialize Google Sheets service and config
        self.sheet_service = GoogleSheetsService()
        self.sheet_config = GOOGLE_SHEETS[SheetName.APPLICATIONS]
        self.sheet_config_archive = GOOGLE_SHEETS[SheetName.ARCHIVE]

        #Pencere ayarları
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.drag_position = QPoint()

        # UI Elements
        self.search_edit = self.findChild(QtWidgets.QLineEdit, "search_edit")
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.all_applications_button = self.findChild(QtWidgets.QPushButton, "pushButton_allaplication")
        self.mentor_meeting_defined_button = self.findChild(QtWidgets.QPushButton, "pushButton_mentormeetingdefined")
        self.mentor_meeting_undefined_button = self.findChild(QtWidgets.QPushButton, "pushButton_mentormeetinundefined")

        # Dropdown ComboBox for filters
        self.comboBox = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.comboBox.clear()
        self.comboBox.addItem("--- Choose Filter ---")  # boş ya da uyarı metni
        self.comboBox.addItems([
            "Prev Vit Check",
            "Filtered Applications",
            "Different Applications",
            "Duplicate Applications"
        ])

        # Table setup
        self.applications_table = self.findChild(QtWidgets.QTableWidget, "tableWidget_application")
        self.back_button = self.findChild(QtWidgets.QPushButton, "pushButton_backmenu")
        self.exit_button = self.findChild(QtWidgets.QPushButton, "pushButton_exit")

        # Set fixed 7 columns for table
        self.table_columns = ["Date", "Name/Surname", "Mail", "Telephone", "Postcode", "State", "Status"]
        self.applications_table.setColumnCount(len(self.table_columns))
        self.applications_table.setHorizontalHeaderLabels(self.table_columns)
        self.applications_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.applications_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Connect UI events
        self.search_button.clicked.connect(self.search_by_name)
        self.search_edit.textChanged.connect(self.search_by_name)  # Live search
        self.all_applications_button.clicked.connect(self.show_all_applications)
        self.mentor_meeting_defined_button.clicked.connect(self.show_mentor_meeting_defined)
        self.mentor_meeting_undefined_button.clicked.connect(self.show_mentor_meeting_undefined)
        self.comboBox.currentTextChanged.connect(self.apply_combo_filter)
        self.back_button.clicked.connect(self.return_to_preferences)
        self.exit_button.clicked.connect(self.close)

        # Load full sheet data and data atchive memory
        self.full_data = []
        self.load_data_from_sheet()
        self.full_data_archive = []
        #self.show_all_applications() sayfa ilk açıldığında tüm app aktif olmasın

    def load_data_from_sheet(self):
        """Load spreadsheet data into memory."""
        data = self.sheet_service.read_data(
            sheet_id=self.sheet_config["sheet_id"],
            range_name=self.sheet_config["ranges"]
        )
        self.full_data = data if data and len(data) >= 2 else []

    def load_archive_data_from_sheet(self):
        """Load spreadsheet data archive into memory."""
        data_archive = self.sheet_service.read_data(
            sheet_id=self.sheet_config_archive["sheet_id"],
            range_name=self.sheet_config_archive["ranges"]
        )
        self.full_data_archive = data_archive if data_archive and len(data_archive) >= 2 else []

    def get_7_columns_data(self, rows):
        """Extract required 7 columns from each row."""
        headers = self.full_data[0]
        mapping = {
            "Date": "Zaman damgası",
            "Name/Surname": "Adınız Soyadınız",
            "Mail": "Mail adresiniz",
            "Telephone": "Telefon Numaranız",
            "Postcode": "Posta Kodunuz",
            "State": "Yaşadığınız Eyalet",
            "Status": "Şu anki durumunuz"
        }

        idx_map = {key: headers.index(full_header) if full_header in headers else -1 for key, full_header in mapping.items()}

        filtered_rows = []
        for row in rows:
            row_data = [str(row[idx]) if idx != -1 and idx < len(row) else "" for key, idx in idx_map.items()]
            filtered_rows.append(row_data)
        return filtered_rows

    def populate_table(self, rows):
        self.applications_table.clearContents()
        self.applications_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # Opsiyonel hizalama
                self.applications_table.setItem(row_idx, col_idx, item)

        self.applications_table.setWordWrap(True)
        self.applications_table.resizeRowsToContents()

    def search_by_name(self):
        """Live search for name starting with input keyword."""
        keyword = self.search_edit.text().strip().lower()
        if not keyword:
            self.applications_table.clearContents()
            self.applications_table.setRowCount(0)
            return

        try:
            name_idx = self.full_data[0].index("Adınız Soyadınız")
        except ValueError:
            name_idx = -1

        filtered_rows = [row for row in self.full_data[1:] if len(row) > name_idx and str(row[name_idx]).lower().startswith(keyword)]
        self.populate_table(self.get_7_columns_data(filtered_rows))

    def show_all_applications(self):
        """Show all application rows."""
        self.populate_table(self.get_7_columns_data(self.full_data[1:]))

    def show_mentor_meeting_defined(self):
        """
        Excel'in U sütununda ('Mentor gorusmesi') değeri 'OK' olan kişileri filtreler
        ve bu başvurulara ait 7 temel sütunu tabloya yazdırır.
        """
        if not self.full_data or len(self.full_data) < 2:
            return  # Veri yoksa çık

        mentor_col_idx = 20  # U sütunu: "Mentor gorusmesi"

        # OK yazan başvuruları filtrele
        filtered_rows = [
            row for row in self.full_data[1:]  # Başlık satırını atla
            if len(row) > mentor_col_idx and str(row[mentor_col_idx]).strip().lower() == "ok"
        ]

        # Sadece ilgili 7 sütunu al
        filtered_7cols = self.get_7_columns_data(filtered_rows)

        # Tabloya yazdır
        self.populate_table(filtered_7cols)

    def show_mentor_meeting_undefined(self):
        """
        Excel'in U sütununda ('Mentor gorusmesi') 'OK' yazmayan başvuruları gösterir.
        Bu kişiler henüz mentor atanmamış olanlardır.
        """
        if not self.full_data or len(self.full_data) < 2:
            return

        mentor_col_idx = 20  # U sütunu

        filtered_rows = [
            row for row in self.full_data[1:]
            if len(row) > mentor_col_idx and str(row[mentor_col_idx]).strip().lower() != "ok"
        ]

        filtered_7cols = self.get_7_columns_data(filtered_rows)
        self.populate_table(filtered_7cols)

    def apply_combo_filter(self):
        selected_filter = self.comboBox.currentText()
        print(f"ComboBox selection: {selected_filter}")

        if selected_filter in ["Filtered Applications", "Different Applications"]:
            self.load_archive_data_from_sheet()

        if selected_filter == "--- Choose Filter ---":
            # Tabloyu temizle ve satır sayısını sıfır yap
            self.applications_table.clearContents()
            self.applications_table.setRowCount(0)
        elif selected_filter == "Prev Vit Check":
            self.show_prev_vit_check()
        elif selected_filter == "Filtered Applications":
            self.show_filtered_applications()
        elif selected_filter == "Different Applications":
            self.show_different_applications()
        elif selected_filter == "Duplicate Applications":
            self.show_duplicate_applications()
        else:
            self.applications_table.clearContents()
            self.applications_table.setRowCount(0)

    def show_prev_vit_check(self):
        """
        Aynı 'Adınız Soyadınız' değerine sahip birden fazla başvuru varsa,
        bu isimleri bulur ve tabloya getirir.
        """
        if not self.full_data or len(self.full_data) < 2:
            return

        name_idx = 1  # B sütunu: 'Adınız Soyadınız'
        name_count = {}
        for row in self.full_data[1:]:
            if len(row) > name_idx:
                name = str(row[name_idx]).strip().lower()
                name_count[name] = name_count.get(name, 0) + 1

        # Tekrar edenleri filtrele
        filtered_rows = [
            row for row in self.full_data[1:]
            if len(row) > name_idx and name_count.get(str(row[name_idx]).strip().lower(), 0) > 1
        ]

        filtered_7cols = self.get_7_columns_data(filtered_rows)
        self.populate_table(filtered_7cols)

    def show_filtered_applications(self):

        if not self.full_data or len(self.full_data) < 2:
            return
        if not self.full_data_archive or len(self.full_data_archive) < 2:
            return

        name_idx = 1  # 'Adınız Soyadınız' sütunu
        archive_names = {
            str(row[name_idx]).strip() for row in self.full_data_archive[1:] if len(row) > name_idx
        }

        filtered_rows = [
            row for row in self.full_data[1:]
            if len(row) > name_idx and str(row[name_idx]).strip() in archive_names
        ]

        filtered_7cols = self.get_7_columns_data(filtered_rows)
        self.populate_table(filtered_7cols)

    def show_different_applications(self):

        if not self.full_data or len(self.full_data) < 2:
            return
        if not self.full_data_archive or len(self.full_data_archive) < 2:
            return

        name_idx = 1  # 'Adınız Soyadınız' sütunu
        archive_names = {
            str(row[name_idx]).strip() for row in self.full_data_archive[1:] if len(row) > name_idx
        }

        filtered_rows = [
            row for row in self.full_data[1:]
            if len(row) > name_idx and str(row[name_idx]).strip() not in archive_names
        ]

        filtered_7cols = self.get_7_columns_data(filtered_rows)
        self.populate_table(filtered_7cols)
    
    def show_duplicate_applications(self):
        """
        Aynı 'Adınız Soyadınız' değerine sahip başvurulardan sadece bir tanesini gösterir.
        Duplicate kayıtları sadeleştirmek için kullanılır.
        """
        if not self.full_data or len(self.full_data) < 2:
            return

        name_idx = 1  # 'Adınız Soyadınız' sütunu

        seen = set()
        unique_rows = []
        for row in self.full_data[1:]:
            if len(row) > name_idx:
                name = str(row[name_idx]).strip().lower()
                if name not in seen:
                    seen.add(name)
                    unique_rows.append(row)

        filtered_7cols = self.get_7_columns_data(unique_rows)
        self.populate_table(filtered_7cols)

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

    def return_to_preferences(self):
        """Return to previous menu depending on user role."""
        print("🔙 Geri butonuna basıldı")
        if self.previous_window:
            self.previous_window.show()
            self.previous_window.raise_()
            self.previous_window.activateWindow()
        self.close()

"""if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationsWindow()
    window.show()
    sys.exit(app.exec())"""