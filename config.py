# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Google API ayarları
# Kimlik dosyasının yolu
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Bağlanılacak Google Sheets API yetki kapsamı
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
]


GOOGLE_SHEETS = {
    "basvuru": {
        "sheet_id": os.getenv("BASVURU_SHEET_ID"),
        "ranges":  "Sayfa1!A:U"
    },
    "mentor": {
        "sheet_id": os.getenv("MENTOR_SHEET_ID"),
        "ranges": "Sayfa1!A:H",
    },
    
    "decision": {
        "sheet_id": os.getenv("MENTOR_SHEET_ID"),
        "ranges":  "Sayfa2!A1:A8"
    },
        
    "interview": {
        "sheet_id": os.getenv("INTERVIEW_SHEET_ID"),
        "ranges": "Sayfa1!A:C",
    },
    "users": {
        "sheet_id": os.getenv("USERS_SHEET_ID"),
        "ranges": "Form Yanıtları 1!A:C",
    }
}
