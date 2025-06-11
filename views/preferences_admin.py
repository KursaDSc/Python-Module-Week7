from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint

class AdminPreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()

        # UI dosyasini yukle
        uic.loadUi(r"ui/preferences_admin.ui", self)

        # Pencereyi cercevesiz ve saydam yap
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.drag_position = QPoint()

        # Butonlara tiklandiginda fonksiyonlari bagla
        self.findChild(QPushButton, "btn_applications").clicked.connect(self.open_applications)
        self.findChild(QPushButton, "btn_mentor").clicked.connect(self.open_mentor_meeting)
        self.findChild(QPushButton, "btn_interviews").clicked.connect(self.open_interviews)
        self.findChild(QPushButton, "btn_admin_menu").clicked.connect(self.open_admin_menu)
        self.findChild(QPushButton, "btn_exit").clicked.connect(self.close)
       

    def open_applications(self):
        from views.applications import ApplicationsWindow
        print("📦 Applications penceresi acilacak")
        self.app_window = ApplicationsWindow(is_admin=True, previous_window=self)
        self.app_window.show()
        self.close()

    def open_mentor_meeting(self):
        from views.mentor import MentorWindow
        print("👩‍🏫 Mentor Meeting penceresi açılacak")
        self.mentor_window = MentorWindow(is_admin=True, previous_window=self)
        self.mentor_window.show()
        self.hide()
        
    def open_interviews(self):
        from views.interviews import InterviewsWindow
        print("🗣️ Interviews penceresi acilacak")
        self.interviews_window = InterviewsWindow(is_admin=True, previous_window=self)
        self.interviews_window.show()
        self.close()

    def open_admin_menu(self):
        from views.admin_menu import AdminMenuWindow
        print("🛠️ Admin Menu açılacak")
        self.admin_menu = AdminMenuWindow()
        self.admin_menu.show()
        self.close()
    
        # Pencereyi mouse ile taşıma fonksiyonları
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
