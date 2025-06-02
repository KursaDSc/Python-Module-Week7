# google_sheets_service.py

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import SERVICE_ACCOUNT_FILE



class GoogleSheetsService:
    def __init__(self):
        self.creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build("sheets", "v4", credentials=self.creds)
        self.sheet = self.service.spreadsheets()

    def read_data(self, sheet_id, range_name: str) -> list[list[str]]:
        """Belirli bir range'den veri okur."""
        try:
            result = self.sheet.values().get(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()
            return result.get("values", [])
        except Exception as e:
            print(f"Veri okuma hatası: {e}")
            return []
    
    def write_sheet(self, sheet_id, range_name, values):
        body = {'values': values}
        result = self.service.values().update(
            spreadsheetId = sheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        return result

    def append_row(self, sheet_id, range_name: str, row_data: list[str]):
        """Yeni bir satır ekler."""
        try:
            self.sheet.values().append(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": [row_data]}
            ).execute()
        except Exception as e:
            print(f"Satır ekleme hatası: {e}")

    def update_cell(self, sheet_id, range_name: str, values: list[list[str]]):
        """Belirli bir range'i topluca günceller (overwrite eder)."""
        try:
            self.sheet.values().update(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body={"values": values}
            ).execute()
        except Exception as e:
            print(f"Hücre güncelleme hatası: {e}")

