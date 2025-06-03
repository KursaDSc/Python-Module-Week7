from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt

from utils.validators import Validator
from views.preferences_admin import AdminPreferencesWindow
from views.preferences import UserPreferencesWindow

from config import GOOGLE_SHEETS, SheetName
from services.google_sheets_service import GoogleSheetsService

class InterviewsWindow(QWidget):
    """
    Interviews window that allows users to manage interview schedules
    and details.
    """

    def __init__(self) -> None:
        """Initialize interviews window and connect signals to actions."""
        super().__init__()
        uic.loadUi(r"ui\interviews.ui", self)  # Load the UI file

        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)