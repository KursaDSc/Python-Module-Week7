from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from views.applications import ApplicationsWindow
from views.mentor import MentorWindow
from views.interviews import InterviewsWindow

class UserPreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(r"ui\preferences.ui", self)  # UI dosyasını yükle
        # Pencereyi çerçevesiz ve saydam yap
        
        # Frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Butonları bağla 
        self.findChild(QPushButton, "btn_mentor").clicked.connect(self.open_mentor_meeting)
        self.findChild(QPushButton, "btn_applications").clicked.connect(self.open_applications)
        self.findChild(QPushButton, "btn_interviews").clicked.connect(self.open_interviews)
        self.findChild(QPushButton, "exitButton").clicked.connect(self.exit_app)

    def open_applications(self):
        print("📄 Applications penceresi acilacak")
        self.applications_window = ApplicationsWindow(is_admin=False, previous_window=self)
        self.applications_window.show()
        self.hide()
    
    def open_mentor_meeting(self):
        print("👩‍🏫 Mentor Meeting penceresi acilacak")
        self.mentor_window = MentorWindow(is_admin=False, previous_window=self)
        self.mentor_window.show()
        self.hide()

    def open_interviews(self):
        print("🗣️ Interviews penceresi acilacak")
        self.interviews_window = InterviewsWindow(is_admin=False, previous_window=self)
        self.interviews_window.show()
        self.hide()

    def exit_app(self):
        # Uygulamadan çıkış
        print("Application closed.")
        self.close()

        if __name__ == "__main__":
            app = QApplication([])
            window = UserPreferencesWindow()
            window.show()
            app.exec()      
# Bu kod, kullanıcı tercihleri penceresini oluşturur ve butonlara tıklama olaylarını bağlar.
# Kullanıcı tercihleri penceresi, kullanıcıların uygulama ayarlarını yönetebileceği bir arayüz sağlar.
# Pencere, çerçevesiz ve saydam olarak ayarlanmıştır. Kullanıcı, geri dönme ve çıkış butonlarına tıklayarak ilgili işlemleri gerçekleştirebilir.
# Bu kod, kullanıcı tercihleri penceresini oluşturur ve butonlara tıklama olaylarını bağlar.
# Kullanıcı tercihleri penceresi, kullanıcıların uygulama ayarlarını yönetebileceği bir arayüz sağlar.
# Pencere, çerçevesiz ve saydam olarak ayarlanmıştır. Kullanıcı, geri dönme ve çıkış butonlarına tıklayarak ilgili işlemleri gerçekleştirebilir.
# Bu kod, kullanıcı tercihleri penceresini oluşturur ve butonlara tıklama olaylarını bağlar.
# Kullanıcı tercihleri penceresi, kullanıcıların uygulama ayarlarını yönetebileceği bir arayüz sağlar.


    