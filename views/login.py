from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt, QThread, QPoint
from workers.data_loader_worker import DatabaseAuthWorker
from widgets.loading import LoadingSpinner
import sys
import os


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        uic.loadUi(resource_path("ui/login.ui"), self)
        self.spinner: LoadingSpinner = LoadingSpinner(self)
        self.spinner.move(150, 150)

        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.drag_position = QPoint()

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
        Handles login logic with database authentication:
        - Runs database query in a background thread.
        - Validates credentials using the returned user row.
        - Opens the appropriate preferences window based on user role.
        """
        self.spinner.start()
        
        # Hazırlanan sorgu
        username = self.usernameField.text()
        password = self.passwordField.text()

        query = "SELECT kullaniciadi, parola, yetki FROM kullanicilar WHERE kullaniciadi = %s"
        params = (username,)

        self.thread = QThread()
        self.worker = DatabaseAuthWorker(query, params, password)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_user_authenticated)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_user_authenticated(self, user) -> None:
        self.spinner.stop()

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
        from views.preferences_admin import AdminPreferencesWindow
        from views.preferences import UserPreferencesWindow
        
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
    import sys
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())