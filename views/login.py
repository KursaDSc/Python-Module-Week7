from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt, QThread
from typing import Optional

from workers.data_loader_worker import DataLoaderWorker
from widgets.loading import LoadingSpinner
from services.auth import authenticate
from views.preferences_admin import AdminPreferencesWindow
from views.preferences import UserPreferencesWindow
from config import GOOGLE_SHEETS, SheetName
from services.google_sheets_service import GoogleSheetsService

class LoginWindow(QWidget):
    """
    Login window that authenticates users via Google Sheets data
    and redirects them to appropriate preference windows based on role.
    """

    def __init__(self) -> None:
        """
        Initializes the login window, loads the UI, and connects signals to actions.
        """
        super().__init__()
        uic.loadUi(r"ui/login.ui", self)
        self.spinner: LoadingSpinner = LoadingSpinner(self)
        self.spinner.move(150, 150)

        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Find widgets by name and cast them to appropriate types
        self.loginButton: QPushButton = self.findChild(QPushButton, "loginButton")
        self.exitButton: QPushButton = self.findChild(QPushButton, "exitButton")
        self.usernameField: QLineEdit = self.findChild(QLineEdit, "usernameField")
        self.passwordField: QLineEdit = self.findChild(QLineEdit, "passwordField")
        self.errorlabel: QLabel = self.findChild(QLabel, "errorlabel")
        self.showPasswordCheckBox: QWidget = self.findChild(QWidget, "showPasswordCheckBox")
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect signals to corresponding methods
        self.showPasswordCheckBox.toggled.connect(self.toggle_password_visibility)
        self.loginButton.clicked.connect(self.login)
        self.exitButton.clicked.connect(self.close_app)
        self.passwordField.returnPressed.connect(self.login)  # Enter key triggers login

    def login(self) -> None:
        """
        Handles login logic:
        - Loads user data from Google Sheets in a background thread.
        - Validates credentials using the loaded user data.
        - Opens the appropriate preferences window based on user role.
        """
        # Spinner starts here, just before Google Sheets call
        self.spinner.start()
        sheet_service = GoogleSheetsService()
        sheet_id = GOOGLE_SHEETS[SheetName.USERS].get("sheet_id")
        range_name = GOOGLE_SHEETS[SheetName.USERS].get("range_name", "A1:C100")

        self.thread = QThread()
        self.worker = DataLoaderWorker(sheet_service, sheet_id, range_name)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_data_loaded_for_login)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_data_loaded_for_login(self, data: list[list[str]]) -> None:
        """
        Slot called when user data is loaded from Google Sheets for authentication.
        Validates credentials, and opens the appropriate preferences window.
        Spinner is stopped only after authentication and before opening the next window.
        """
        if not data:
            self.spinner.stop()
            self.errorlabel.setText("No user data found!")
            return

        user = authenticate(self.usernameField.text(), self.passwordField.text(), data)
        if user:
            self.errorlabel.setText(f"Login successful! Role: {user.role}")
            self.spinner.stop()  # Stop spinner just before opening the next window
            self.open_preferences(user.role)
        else:
            self.spinner.stop()
            self.errorlabel.setText("Invalid username or password!")
            self.usernameField.clear()
            self.passwordField.clear()

    def open_preferences(self, role: str) -> None:
        """
        Opens the appropriate preferences window based on user role.

        Args:
            role (str): The role of the user, either "admin" or "user".
        """
        if role == "admin":
            self.preferences_window = AdminPreferencesWindow()
        else:
            self.preferences_window = UserPreferencesWindow()

        self.preferences_window.show()
        self.close()

    def close_app(self) -> None:
        """
        Exits the application.
        """
        QApplication.quit()

    def toggle_password_visibility(self, checked: bool) -> None:
        """
        Toggles password visibility in the password input field.

        Args:
            checked (bool): Whether the checkbox is checked (True to show password).
        """
        if checked:
            self.passwordField.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())