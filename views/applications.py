import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint
from services.db import get_data_list

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ApplicationsWindow(QtWidgets.QMainWindow):
    def __init__(self, is_admin=False, previous_window=None):
        super().__init__()
        uic.loadUi(resource_path("ui/applications.ui"), self)
        self.previous_window = previous_window
        self.is_admin = is_admin
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.drag_position = QPoint()

        # UI bileşenleri
        self.search_edit = self.findChild(QtWidgets.QLineEdit, "search_edit")
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.all_applications_button = self.findChild(QtWidgets.QPushButton, "pushButton_allaplication")
        self.mentor_meeting_defined_button = self.findChild(QtWidgets.QPushButton, "pushButton_mentormeetingdefined")
        self.mentor_meeting_undefined_button = self.findChild(QtWidgets.QPushButton, "pushButton_mentormeetinundefined")
        self.comboBox = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.applications_table = self.findChild(QtWidgets.QTableWidget, "tableWidget_application")
        self.back_button = self.findChild(QtWidgets.QPushButton, "pushButton_backmenu")
        self.exit_button = self.findChild(QtWidgets.QPushButton, "pushButton_exit")

        self.comboBox.clear()
        self.comboBox.addItem("--- Choose Filter ---")
        self.comboBox.addItems([
            "Prev Vit Check",
            "Filtered Applications",
            "Different Applications",
            "Duplicate Applications"
        ])

        # Tablo yapılandırma
        cols = ["Date", "Name/Surname", "Mail", "Telephone", "Postcode", "State", "Status"]
        self.applications_table.setColumnCount(len(cols))
        self.applications_table.setHorizontalHeaderLabels(cols)
        self.applications_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.applications_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Olay bağlama
        self.search_button.clicked.connect(self.search_by_name)
        self.search_edit.textChanged.connect(self.search_by_name)
        self.all_applications_button.clicked.connect(self.show_all_applications)
        self.mentor_meeting_defined_button.clicked.connect(self.show_mentor_meeting_defined)
        self.mentor_meeting_undefined_button.clicked.connect(self.show_mentor_meeting_undefined)
        self.comboBox.currentTextChanged.connect(self.apply_combo_filter)
        self.back_button.clicked.connect(self.return_to_preferences)
        self.exit_button.clicked.connect(self.close)

    # Merkez SQL sorgu metodu
    def load_data_from_db(self, period=None, mentor_status=None):
        base = """
            SELECT
                b.basvuruid,
                k.adsoyad,
                b.zamandamgasi,
                b.suankidurum,
                k.mailadresi,
                k.telefonnumarasi,
                k.postakodu,
                k.yasadiginizeyalet
            FROM basvurular b
            JOIN kursiyerler k USING(kursiyerid)
            """

        # Mentor durumu için LEFT JOIN gerekli
        if mentor_status is not None:
            base += " LEFT JOIN mentortablosu m USING(kursiyerid) "

        conditions = []
        if period:
            conditions.append(f"b.basvurudonemi = '{period}'")
        if mentor_status is not None:
            if mentor_status:
                conditions.append("m.kursiyerid IS NOT NULL")
            else:
                conditions.append("m.kursiyerid IS NULL")

        query = base
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return get_data_list(query)

    def get_7_columns_data(self, rows):
        result = []
        for r in rows:
            result.append([
                str(r[2]),  # zamandamgasi → Date
                str(r[1]),  # adsoyad → Name/Surname
                str(r[4]),  # mail
                str(r[5]),  # telefon
                str(r[6]),  # postakodu
                str(r[7]),  # eyalet
                str(r[3])   # suankidurum → Status
            ])
        return result

    def populate_table(self, rows):
        self.applications_table.clearContents()
        self.applications_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                item = QtWidgets.QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                self.applications_table.setItem(i, j, item)
        self.applications_table.resizeRowsToContents()

    # Filtre fonksiyonları: her biri kendi SQL ile çalışıyor
    def show_all_applications(self):
        data = self.load_data_from_db(period="VIT-8")
        self.populate_table(self.get_7_columns_data(data))
        self.full_data = data

    def show_mentor_meeting_defined(self):
        data = self.load_data_from_db(period="VIT-8", mentor_status=1)
        self.populate_table(self.get_7_columns_data(data))

    def show_mentor_meeting_undefined(self):
        data = self.load_data_from_db(period="VIT-8", mentor_status=0)
        self.populate_table(self.get_7_columns_data(data))

    def search_by_name(self):
        kw = self.search_edit.text().strip().lower()
        if not kw:
            return
        data = self.load_data_from_db(period="VIT-8")  # ya da bir cache
        filtered = [r for r in data if str(r[1]).lower().startswith(kw)]
        self.populate_table(self.get_7_columns_data(filtered))

    def apply_combo_filter(self, txt):
        period = "VIT-8"
        if txt == "Prev Vit Check":
            data = self.load_data_from_db(period=None)  # tüm dönemler
            names = [str(r[1]).strip().lower() for r in data]
            duplicates = {n for n in names if names.count(n) > 1}
            out = [r for r in data if str(r[1]).strip().lower() in duplicates]
            self.populate_table(self.get_7_columns_data(out))
        elif txt == "Filtered Applications":
            self.show_all_applications()
        elif txt == "Different Applications":
            all_data = self.load_data_from_db(period=None)
            vit8_names = {str(r[1]).strip().lower() for r in self.load_data_from_db("VIT-8")}
            out = [r for r in all_data if str(r[1]).strip().lower() not in vit8_names]
            self.populate_table(self.get_7_columns_data(out))
        elif txt == "Duplicate Applications":
            data = self.load_data_from_db(period="VIT-8")
            names = [str(r[1]).strip().lower() for r in data]
            unique = []
            seen = set()
            for r in data:
                n = str(r[1]).strip().lower()
                if n not in seen:
                    seen.add(n)
                    unique.append(r)
            self.populate_table(self.get_7_columns_data(unique))
        else:
            return

    def return_to_preferences(self):
        if self.previous_window:
            self.previous_window.show()
        self.close()

    def closeEvent(self, e):
        if self.previous_window: self.previous_window.show()
        e.accept()

    def mousePressEvent(self, evt):
        if evt.button() == Qt.MouseButton.LeftButton:
            self.drag_position = evt.globalPosition().toPoint() - self.frameGeometry().topLeft()
            evt.accept()

    def mouseMoveEvent(self, evt):
        if evt.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(evt.globalPosition().toPoint() - self.drag_position)
            evt.accept()

    def mouseReleaseEvent(self, evt):
        self.drag_position = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ApplicationsWindow()
    w.show()
    sys.exit(app.exec())
