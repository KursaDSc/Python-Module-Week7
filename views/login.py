from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt

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
        """Initialize login window and connect signals to actions."""
        super().__init__()
        uic.loadUi(r"ui\login.ui", self)  # Load the UI file

        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ✅ Find widgets by name and cast them to appropriate types
        self.loginButton: QPushButton = self.findChild(QPushButton, "loginButton")
        self.exitButton: QPushButton = self.findChild(QPushButton, "exitButton")
        self.usernameField: QLineEdit = self.findChild(QLineEdit, "usernameField")
        self.passwordField: QLineEdit = self.findChild(QLineEdit, "passwordField")
        self.errorlabel: QLabel = self.findChild(QLabel, "errorlabel")
        self.showPasswordCheckBox: QWidget = self.findChild(QWidget, "showPasswordCheckBox")
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)  # Initially hide password

        # Connect signals to corresponding methods
        self.showPasswordCheckBox.toggled.connect(self.toggle_password_visibility)
        self.loginButton.clicked.connect(self.login)
        self.exitButton.clicked.connect(self.close_app)
        
        
    def get_users_data(self) -> list[list[str]]:
        """
        Fetches user data from the Google Sheets document specified in the configuration.

        Returns:
            list[list[str]]: A list of rows, each row being a list of string cell values
                            fetched from the Google Sheet's user data range.
        """
        # Initialize Google Sheets service
        sheet_service = GoogleSheetsService()
        sheet_id = GOOGLE_SHEETS[SheetName.USERS].get("sheet_id")
        range_name = GOOGLE_SHEETS[SheetName.USERS].get("range_name", "A1:C100")  # Default range if not specified
        users = sheet_service.read_data(sheet_id, range_name)
        return users


    def login(self) -> None:
        """
        Handles login logic:
        - Reads user data from Google Sheets.
        - Validates credentials.
        - Opens appropriate preferences window based on user role.
        """

        # Read user data from Google Sheets
        users = self.get_users_data()
        if not users:
            self.errorlabel.setText("No user data found!")
            return

        user = authenticate(self.usernameField.text(), self.passwordField.text(), users)
        if user:
            self.errorlabel.setText(f"Login successful! Role: {user.role}")
            self.open_preferences(user.role)
        else:
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
        """Exits the application."""
        QApplication.quit()

    def toggle_password_visibility(self, checked: bool) -> None:
        """
        Toggles password visibility in the password input field.
        
        Args:
            checked (bool): Whether the checkbox is checked (True to show password).
        """
        if checked:
            self.passwordField.setEchoMode(QLineEdit.EchoMode.Normal)  # Show password
        else:
            self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())