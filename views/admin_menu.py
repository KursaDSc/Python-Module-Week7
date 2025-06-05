from PyQt6.QtWidgets import QWidget, QPushButton, QTableWidget, QApplication, QTableWidgetItem, QSizeGrip
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint

from utils.validators import Validator
from services.google_calendar_service import GoogleCalendarService
from services.email_service import send_email_to


class AdminMenuWindow(QWidget):
    """
    Admin panel window for managing calendar events and sending emails.

    Features:
        - Display upcoming Google Calendar events in a table.
        - Placeholder functionality for sending emails.
        - Navigation control to return to preferences or exit the app.
    """

    def __init__(self) -> None:
        """
        Initializes the admin panel UI, sets up the window behavior,
        and connects UI buttons to corresponding event handler methods.
        """
        super().__init__()
        uic.loadUi(r"ui\admin_panel.ui", self)  # Load the UI file
        
        self.data = self.get_events()

        # Frameless pencere ayarı
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Sürükleme için pozisyon başlangıcı
        self.drag_position = QPoint()

        # Sağ alt köşeye yeniden boyutlandırma aracı ekle
        self.resize_grip = QSizeGrip(self)
        self.resize_grip.setStyleSheet("background: transparent;")
        self.resize_grip.resize(16, 16)

        # Retrieve and cast UI widgets
        self.activityButton: QPushButton = self.findChild(QPushButton, "activityButton")
        self.emailButton: QPushButton = self.findChild(QPushButton, "emailButton")
        self.returnButton: QPushButton = self.findChild(QPushButton, "returnButton")
        self.exitButton: QPushButton = self.findChild(QPushButton, "exitButton")
        self.activityTable: QTableWidget = self.findChild(QTableWidget, "activityTable")

        # Connect buttons to handler functions
        self.activityButton.clicked.connect(self.show_calendar_events)
        self.emailButton.clicked.connect(self.send_emails_to_attendees)
        self.returnButton.clicked.connect(self.return_to_preferences)
        self.exitButton.clicked.connect(self.close_app)
        
    def get_events(self) -> list:
        """
        Fetches upcoming calendar events from Google Calendar.

        Returns:
            list: A list of event objects containing event details.
        """
        calendar_service = GoogleCalendarService('credentials.json')
        events_raw = calendar_service.list_events(max_results=20)
        return [calendar_service.event_from_api(e) for e in events_raw]

    def show_calendar_events(self) -> None:
        """
        Displays the upcoming calendar events in the activity table.
        """
        self.activityTable.setRowCount(len(self.data))
        for row, event in enumerate(self.data):
            self.activityTable.setItem(row, 0, QTableWidgetItem(event.title))
            self.activityTable.setItem(row, 1, QTableWidgetItem(event.start_time))
            self.activityTable.setItem(row, 2, QTableWidgetItem(event.attendee_email))
            self.activityTable.setItem(row, 3, QTableWidgetItem(event.organizer_email))


    def send_emails_to_attendees(self) -> None:
        """
        Collects unique attendee email addresses from the activity table
        and sends an informational email to each valid address.

        This method assumes that the attendee email addresses are located
        in the third column (index 2) of the QTableWidget.

        Invalid or missing values like 'N/A' or 'Yok' are ignored.
        """
        attendee_emails: set[str] = set()
        row_count: int = self.activityTable.rowCount()

        for row in range(row_count):
            email_item = self.activityTable.item(row, 2)  # Column index 2: Attendee Email
            if email_item:
                email = email_item.text().strip()
                if Validator.validate_email(email):
                    attendee_emails.add(email)

        for email in attendee_emails:
            send_email_to(email, subject="Event Notification", body="You are invited to the event.")

    def return_to_preferences(self) -> None:
        """
        Placeholder for returning to the preferences window.
        Replace with navigation logic to switch windows.
        """
        print("Return to preferences window is not implemented yet.")

    def close_app(self) -> None:
        """
        Closes the application.
        """
        QApplication.quit()
        
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

    def handle_back(self):
        from views.preferences_admin import PreferencesAdminWindow
        self.preferences_window = PreferencesAdminWindow()
        self.preferences_window.show()
        self.close()


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    app = QApplication(sys.argv)
    window = AdminMenuWindow()
    window.show()
    sys.exit(app.exec())
