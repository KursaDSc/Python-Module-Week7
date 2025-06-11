from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication

class UserPreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(r"ui\preferences.ui", self)  # UI dosyasını yükle
        # Pencereyi çerçevesiz ve saydam yap
        
        # Frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.drag_position = QPoint()

        # Butonları bağla 
        self.findChild(QPushButton, "btn_mentor").clicked.connect(self.open_mentor_meeting)
        self.findChild(QPushButton, "btn_applications").clicked.connect(self.open_applications)
        self.findChild(QPushButton, "btn_interviews").clicked.connect(self.open_interviews)
        self.findChild(QPushButton, "exitButton").clicked.connect(self.exit_app)

    def open_applications(self):
        from views.applications import ApplicationsWindow  # <-- import buraya taşındı
        print("📄 Applications penceresi acilacak")
        self.applications_window = ApplicationsWindow(is_admin=False, previous_window=self)
        self.applications_window.show()
        self.hide()
    
    def open_mentor_meeting(self):
        from views.mentor import MentorWindow
        print("👩‍🏫 Mentor Meeting penceresi acilacak")
        self.mentor_window = MentorWindow(is_admin=False, previous_window=self)
        self.mentor_window.show()
        self.hide()

    def open_interviews(self):
        from views.interviews import InterviewsWindow
        print("🗣️ Interviews penceresi acilacak")
        self.interviews_window = InterviewsWindow(is_admin=False, previous_window=self)
        self.interviews_window.show()
        self.hide()

    def exit_app(self):
        # Uygulamadan çıkış
        print("Application closed.")
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


    