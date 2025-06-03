from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt

from utils.validators import Validator


from config import GOOGLE_SHEETS, SheetName
from services.google_sheets_service import GoogleSheetsService

class ApplicationsWindow(QWidget):
    """
    Login window that authenticates users via Google Sheets data
    and redirects them to appropriate preference windows based on role.
    """

    def __init__(self) -> None:
        """Initialize login window and connect signals to actions."""
        super().__init__()
        uic.loadUi(r"ui\applications.ui", self)  # Load the UI file

        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        pass