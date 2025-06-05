from PyQt6.QtWidgets import QWidget, QPushButton, QTableWidget, QApplication, QTableWidgetItem, QSizeGrip
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint, QThread

# views/admin_menu.py içinde
from services.google_calendar_service import DEFAULT_CALENDAR_ID

from workers.sheets_loader_worker import SheetsLoaderWorker
from workers.email_sender_worker import EmailSenderWorker

from widgets.loading import LoadingSpinner
from utils.validators import Validator
from services.google_calendar_service import GoogleCalendarService
from services.email_service import send_email_to

class AdminMenuWindow(QWidget):
    """
    Admin panel window for managing calendar events and sending emails.
    """

    def __init__(self) -> None:
        """
        Initializes the admin panel UI, sets up the window behavior,
        and connects UI buttons to corresponding event handler methods.
        """
        super().__init__()
        uic.loadUi(r"ui/admin_panel.ui", self)
        self.spinner = LoadingSpinner(self)
        self.spinner.center_in_parent()

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


    def show_calendar_events(self) -> None:
        self.spinner.start()
        self.spinner.center_in_parent()
        sheet_service = GoogleCalendarService('credentials.json')
        calendar_id = DEFAULT_CALENDAR_ID  # .env'den gelen değer
        self.thread = QThread()
        self.worker = SheetsLoaderWorker(sheet_service, calendar_id, None)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_events_loaded)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_events_loaded(self, events_raw: list) -> None:
        """
        Called when events are loaded from Google Calendar.
        Populates the table and stops the spinner.
        """
        self.spinner.stop()
        calendar_service = GoogleCalendarService('credentials.json')
        self.data = [calendar_service.event_from_api(e) for e in events_raw]
        self.activityTable.setRowCount(len(self.data))
        for row, event in enumerate(self.data):
            self.activityTable.setItem(row, 0, QTableWidgetItem(event.title))
            self.activityTable.setItem(row, 1, QTableWidgetItem(event.start_time))
            self.activityTable.setItem(row, 2, QTableWidgetItem(event.attendee_email))
            self.activityTable.setItem(row, 3, QTableWidgetItem(event.organizer_email))

    def send_emails_to_attendees(self) -> None:
        """
        Collects unique attendee email addresses from the activity table
        and sends an informational email to each valid address in a background thread.
        """
        attendee_emails: set[str] = set()
        row_count: int = self.activityTable.rowCount()
        for row in range(row_count):
            email_item = self.activityTable.item(row, 2)
            if email_item:
                email = email_item.text().strip()
                if Validator.validate_email(email):
                    attendee_emails.add(email)

        if not attendee_emails:
            return

        self.spinner.start()
        self.spinner.center_in_parent()
        self.thread = QThread()
        self.worker = EmailSenderWorker(
            list(attendee_emails),
            "Event Notification",
            "You are invited to the event.",
            send_email_to
        )
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_emails_sent)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_emails_sent(self) -> None:
        """
        Called when all emails have been sent. Stops the spinner.
        """
        self.spinner.stop()
        # Optionally show a message to the user

    def return_to_preferences(self) -> None:
        from views.preferences_admin import AdminPreferencesWindow
        self.preferences_window = AdminPreferencesWindow()
        self.preferences_window.show()
        self.close()

    def close_app(self) -> None:
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

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    app = QApplication(sys.argv)
    window = AdminMenuWindow()
    window.show()
    sys.exit(app.exec())