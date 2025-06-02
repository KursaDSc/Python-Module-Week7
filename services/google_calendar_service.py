from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()
calendar_id = os.getenv("GOOGLE_CALENDAR_ID")

class GoogleCalendarService:
    def __init__(self, credentials_file: str, scopes: list[str] = None):
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        self.creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_events(self, calendar_id: str = calendar_id, max_results: int = 20):
        events_result = self.service.events().list(
            calendarId=calendar_id,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])