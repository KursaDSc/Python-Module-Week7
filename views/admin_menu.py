from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QTableWidget, QApplication, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt

from utils.validators import Validator
from services.google_calendar_service import GoogleCalendarService
from services.email_service import send_email_to, event_from_api


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

        # Configure window to be frameless and transparent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

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

    def show_calendar_events(self) -> None:
        """
        Fetches upcoming Google Calendar events and displays them
        in a table widget. Each row includes event title, start time,
        attendee email, and organizer email.
        """
        calendar_service = GoogleCalendarService('credentials.json')
        events_raw = calendar_service.list_events(max_results=20)
        events = [event_from_api(e) for e in events_raw]

        self.activityTable.setRowCount(len(events))
        for row, event in enumerate(events):
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


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AdminMenuWindow()
    window.show()
    sys.exit(app.exec())
