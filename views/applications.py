import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS, SheetName
from views.mentor import MentorWindow
from views.admin_menu import AdminMenuWindow
from views.preferences import UserPreferencesWindow
from views.preferences_admin import AdminPreferencesWindow

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
    def __init__(self, is_admin=False):
        super().__init__()
        uic.loadUi("ui/applications.ui", self)

        self.is_admin = is_admin

        # Initialize Google Sheets service and config
        self.sheet_service = GoogleSheetsService()
        self.sheet_config = GOOGLE_SHEETS[SheetName.APPLICATIONS]

        # UI Elements
        self.search_edit = self.findChild(QtWidgets.QLineEdit, "search_edit")
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.all_applications_button = self.findChild(QtWidgets.QPushButton, "pushButton_allaplication")
        self.mentor_meeting_defined_button = self.findChild(QtWidgets.QPushButton, "pushButton_mentormeetingdefined")
        self.mentor_meeting_undefined_button = self.findChild(QtWidgets.QPushButton, "pushButton_mentormeetinundefined")

        # Dropdown ComboBox for filters
        self.comboBox = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.comboBox.clear()
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

        # Load full sheet data into memory
        self.full_data = []
        self.load_data_from_sheet()
        self.show_all_applications()

    def load_data_from_sheet(self):
        """Load spreadsheet data into memory."""
        data = self.sheet_service.read_data(
            sheet_id=self.sheet_config["sheet_id"],
            range_name=self.sheet_config["ranges"]
        )
        self.full_data = data if data and len(data) >= 2 else []

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
        """Populate table with processed data rows."""
        self.applications_table.clearContents()
        self.applications_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.applications_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(value))

    def search_by_name(self):
        """Live search for name starting with input keyword."""
        keyword = self.search_edit.text().strip().lower()
        if not keyword:
            self.show_all_applications()
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

        if selected_filter == "Prev Vit Check":
            self.show_prev_vit_check()
        elif selected_filter == "Filtered Applications":
            self.show_filtered_applications()
        elif selected_filter == "Different Applications":
            self.show_different_applications()
        elif selected_filter == "Duplicate Applications":
            self.show_duplicate_applications()
        else:
            # ComboBox içinde olmayan bir seçim olursa tabloyu temizle veya tümünü göster
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
        """
        VIT1 ve VIT2 listelerindeki isimlerle eşleşen başvuruları getirir.
        Bu isimler gelecekte dış kaynaklı listelerle karşılaştırmak içindir.
        Şu an her iki liste boştur, bu yüzden sonuç da boştur.
        """
        if not self.full_data or len(self.full_data) < 2:
            return

        vit1 = set()  # Gelecekte eklenecek dış liste
        vit2 = set()

        name_idx = 1  # 'Adınız Soyadınız' sütunu

        filtered_rows = [
            row for row in self.full_data[1:]
            if len(row) > name_idx and str(row[name_idx]).strip() in vit1.union(vit2)
        ]

        filtered_7cols = self.get_7_columns_data(filtered_rows)
        self.populate_table(filtered_7cols)

    def show_different_applications(self):
        """
        VIT1 ve VIT2 listelerinde olmayan başvuruları gösterir.
        Şu an her iki liste boştur, bu yüzden tüm başvurular listelenir.
        """
        if not self.full_data or len(self.full_data) < 2:
            return

        vit1 = set()  # Gelecekte eklenecek dış liste
        vit2 = set()

        name_idx = 1  # 'Adınız Soyadınız' sütunu

        filtered_rows = [
            row for row in self.full_data[1:]
            if len(row) > name_idx and str(row[name_idx]).strip() not in vit1.union(vit2)
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

    def return_to_preferences(self):
        """Return to previous menu depending on user role."""
        if self.is_admin:
            self.pref_window = UserPreferencesWindow()
        else:
            self.pref_window = UserPreferencesWindow()
        self.pref_window.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationsWindow()
    window.show()
    sys.exit(app.exec())