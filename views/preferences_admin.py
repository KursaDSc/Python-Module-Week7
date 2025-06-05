from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt

from views.applications import ApplicationsWindow
from views.mentor import MentorWindow
from views.interviews import InterviewsWindow
from views.applications import ApplicationsWindow
from views.admin_menu import AdminMenuWindow

class AdminPreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()

        # UI dosyasini yukle
        uic.loadUi(r"ui/preferences_admin.ui", self)

        # Pencereyi cercevesiz ve saydam yap
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Butonlara tiklandiginda fonksiyonlari bagla
        self.findChild(QPushButton, "btn_applications").clicked.connect(self.open_applications)
        self.findChild(QPushButton, "btn_mentor").clicked.connect(self.open_mentor_meeting)
        self.findChild(QPushButton, "btn_interviews").clicked.connect(self.open_interviews)
        self.findChild(QPushButton, "btn_admin_menu").clicked.connect(self.open_admin_menu)
        self.findChild(QPushButton, "btn_exit").clicked.connect(self.close)
       

    def open_applications(self):
        print("📦 Applications penceresi acilacak")
        self.app_window = ApplicationsWindow()
        self.app_window.show()
        self.close()

    def open_mentor_meeting(self):
        print("👩‍🏫 Mentor Meeting penceresi açılacak")
        self.mentor_window = MentorWindow(is_admin=True, previous_window=self)
        self.mentor_window.show()
        self.hide()
        
    def open_interviews(self):
        print("🗣️ Interviews penceresi acilacak")
        self.interviews_window = InterviewsWindow()
        self.interviews_window.show()
        self.close()

    def open_admin_menu(self):
     
        print("🛠️ Admin Menu açılacak")
        self.admin_menu = AdminMenuWindow()
        self.admin_menu.show()
        self.close()
