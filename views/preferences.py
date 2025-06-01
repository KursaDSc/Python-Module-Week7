from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class UserPreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"ui\preferences.ui", self)  # UI dosyasını yükle
        
        # Frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)