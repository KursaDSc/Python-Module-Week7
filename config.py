# config.py
import os

# Google API ayarları
# Kimlik dosyasının yolu
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Bağlanılacak Google Sheets API yetki kapsamı
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "your_google_sheet_id_here")
GOOGLE_SHEET_RANGE = {
    "applicants": "Applicants!A2:Z",
    "appointments": "Appointments!A2:D",
    "users": "Users!A2:E"
}

GOOGLE_SHEETS = {
    "basvuru": {
        "sheet_id": os.getenv("BASVURU_SHEET_ID", "1ynkCpTSAY_didqRFrCCTLDrsMkUERu0KzLQF5yNj0_0"),
        "ranges":  "Sayfa1!A:U"
    },
    "mentor": {
        "sheet_id": os.getenv("MENTOR_SHEET_ID", "1hlv5xC4rMQ2wJ1Fdos-Y5E44d4jAY4uJ1TtfMYg_m6s"),
        "ranges": "Sayfa1!A:H",
    },
    
    "decision": {
        "sheet_id": os.getenv("MENTOR_SHEET_ID", "1hlv5xC4rMQ2wJ1Fdos-Y5E44d4jAY4uJ1TtfMYg_m6s"),
        "ranges":  "Sayfa2!A1:A8"
    },
        
    "interview": {
        "sheet_id": os.getenv("INTERVIEW_SHEET_ID", "1gGOcbbriNvTLjWi9Q6O2AsUCd0PJk9tNV_ZVbyr0wCk"),
        "ranges": "Sayfa1!A:C",
    },
    "users": {
        "sheet_id": os.getenv("USERS_SHEET_ID", "1E5DPYXINRTq4M15FZq2L8rOLo6Br_WzmLU4VDTOBfXE"),
        "ranges": "Form Yanıtları 1!A:C",
    }
}


# Uygulama ayarları
APP_NAME = "Başvuru Takip Sistemi"
IS_DEBUG = True