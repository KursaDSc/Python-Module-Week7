import os
from dotenv import load_dotenv
from typing import TypedDict, Dict
from enum import Enum

load_dotenv()


SERVICE_ACCOUNT_FILE = 'credentials.json'


class SheetConfig(TypedDict):
    sheet_id: str
    ranges: str


class SheetName(str, Enum):
    APPLICATIONS = "applications"
    ARCHIVE = "archive"
    MENTOR = "mentor"
    DECISION = "decision"
    INTERVIEW = "interview"
    USERS = "users"


GOOGLE_SHEETS: Dict[SheetName, SheetConfig] = {
    SheetName.APPLICATIONS: {
        "sheet_id": os.getenv("BASVURU_SHEET_ID", ""),
        "ranges": "Sayfa1!A:U",
    },
    SheetName.ARCHIVE: {
        "sheet_id": os.getenv("YEDEK_SHEET_ID", ""),
        "ranges": "Sayfa1!A:U",
    },
    SheetName.MENTOR: {
        "sheet_id": os.getenv("MENTOR_SHEET_ID", ""),
        "ranges": "Sayfa1!A:H",
    },
    SheetName.DECISION: {
        "sheet_id": os.getenv("MENTOR_SHEET_ID", ""),
        "ranges": "Sayfa2!A1:A8",
    },
    SheetName.INTERVIEW: {
        "sheet_id": os.getenv("INTERVIEW_SHEET_ID", ""),
        "ranges": "Sayfa1!A:C",
    },
    SheetName.USERS: {
        "sheet_id": os.getenv("USERS_SHEET_ID", ""),
        "ranges": "Form Yanıtları 1!A:C",
    },
}