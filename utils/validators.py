from services.google_sheets_service import GoogleSheetsService
from config import GOOGLE_SHEETS

sheet_service = GoogleSheetsService()

def validate_user(input_username, input_password):
    """
    Kullanıcı adı ve parola doğrulaması yapar.
    users_db: {'kullanici_adi': {'password': 'parola', 'role': 'admin/normal'}}
    Doğruysa rolünü döner, yanlışsa None döner.
    """
    try:
        input_username = input_username.strip()
        input_password = input_password.strip()
        sheet = GOOGLE_SHEETS["users"]
        print(f"Doğrulama için sheet bilgisi: {sheet}")
        users = sheet_service.read_data(sheet["sheet_id"], sheet["ranges"])

        for user in users:
            username, password, role = user
            if username == input_username and password == input_password:
                return role
        return None
    except Exception as e:
        print(f"Kullanıcı doğrulama hatası: {e}")
        return None