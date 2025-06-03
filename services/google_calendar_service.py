from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
from typing import List, Optional

load_dotenv()

DEFAULT_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")


class GoogleCalendarService:
    """
    A service class for interacting with Google Calendar API.

    Allows listing upcoming events from a specified Google Calendar.
    """

    def __init__(self, credentials_file: str, scopes: Optional[List[str]] = None) -> None:
        """
        Initializes the Google Calendar service.

        Args:
            credentials_file (str): Path to the service account credentials JSON file.
            scopes (Optional[List[str]]): List of scopes for the Google API. Defaults to readonly access.
        """
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/calendar.readonly']

        self.creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_events(self, calendar_id: Optional[str] = None, max_results: int = 20) -> List[dict]:
        """
        Lists upcoming events from a Google Calendar.

        Args:
            calendar_id (Optional[str]): The ID of the calendar to query. Defaults to the one set in environment variable.
            max_results (int): The maximum number of events to retrieve.

        Returns:
            List[dict]: A list of event dictionaries from the calendar.
        """
        calendar_id = calendar_id or DEFAULT_CALENDAR_ID

        events_result = self.service.events().list(
            calendarId=calendar_id,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])
