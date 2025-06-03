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
        self.findChild(QPushButton, "btn_exit").clicked.connect(self.exit_app)
        
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


    