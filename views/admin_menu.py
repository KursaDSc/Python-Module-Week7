from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QTableWidget, QApplication, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt

from services.google_calendar_service import GoogleCalendarService

class AdminMenuWindow(QWidget):
    """
    Login window that authenticates users via Google Sheets data
    and redirects them to appropriate preference windows based on role.
    """

    def __init__(self) -> None:
        """Initialize login window and connect signals to actions."""
        super().__init__()
        uic.loadUi(r"ui\admin_panel.ui", self)  # Load the UI file

        # Set frameless and transparent window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ✅ Find widgets by name and cast them to appropriate types
        self.activityButton: QPushButton = self.findChild(QPushButton, "activityButton")
        self.emailButton: QPushButton = self.findChild(QPushButton, "emailButton")
        self.returnButton: QPushButton = self.findChild(QPushButton, "returnButton")
        self.exitButton: QPushButton = self.findChild(QPushButton, "exitButton")
        self.activityTable: QTableWidget = self.findChild(QTableWidget, "activityTable")


        # Connect signals to corresponding methods
        self.activityButton.clicked.connect(self.show_calendar_events)
        self.emailButton.clicked.connect(self.send_email)
        self.returnButton.clicked.connect(self.return_to_preferences)
        self.exitButton.clicked.connect(self.close_app)
        
        
    def show_calendar_events(self) -> None:
        # GoogleCalendarService ile etkinlikleri al
        calendar_service = GoogleCalendarService('credentials.json')
        events = calendar_service.list_events(max_results=20)
        print(f"Etkinlikler: {events}")

        # TableWidget ayarları
        self.activityTable.setRowCount(len(events))
        self.activityTable.setColumnCount(4)
        self.activityTable.setHorizontalHeaderLabels([
            "Etkinlik Adı", "Başlangıç Zamanı", "Katılımcı E-Maili", "Organizatör E-Maili"
        ])

        for row, event in enumerate(events):
            event_name = event.get('summary', 'Yok')
            start_time = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'Yok'))
            organizer_email = event.get('organizer', {}).get('email', 'Yok')
            attendees = event.get('attendees', [])
            attendee_email = attendees[0]['email'] if attendees else 'Yok'

            self.activityTable.setItem(row, 0, QTableWidgetItem(event_name))
            self.activityTable.setItem(row, 1, QTableWidgetItem(start_time))
            self.activityTable.setItem(row, 2, QTableWidgetItem(attendee_email))
            self.activityTable.setItem(row, 3, QTableWidgetItem(organizer_email))

    def send_email(self) -> None:
        """
        Placeholder method for sending emails.
        This should be implemented with actual email sending logic.
        """
        print("Email gönderme işlevi henüz uygulanmadı.")
        
    def return_to_preferences(self) -> None:
        """
        Returns to the preferences window.
        This should be implemented with actual logic to return to the preferences.
        """
        print("Tercihler penceresine dönme işlevi henüz uygulanmadı.")
                 
    
    def close_app(self) -> None:
        """Exits the application."""
        QApplication.quit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AdminMenuWindow()
    window.show()
    sys.exit(app.exec())