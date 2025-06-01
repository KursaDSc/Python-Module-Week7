import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_google_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def get_file_path(filename):
    """
    Get the absolute path of a file in the current directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

def read_json(file):
    filepath = get_file_path(file)
    if not os.path.exists(filepath):
        print("Dosya yok:", filepath)
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
            if not data.strip():
                print("Dosya boş.")
                return []
            return json.loads(data)
    except json.JSONDecodeError as e:
        print("JSON hatası:", e)
        return []



#json dosyasina yaz
def write_json(file, data):
     filepath = get_file_path(file)
     with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# JSON dosyasına veri ekle (liste yapısında ise)
def append_to_json_file(filepath, new_data):
    data = read_json(filepath)
    if isinstance(data, list):
        data.append(new_data)
    else:
        data = [new_data]
    write_json(filepath, data)

# Belirli bir öğeyi (kimlik,tbaslik, isim vs.) sil (liste içindeki sözlük)
#chatgpt`den buldum
def delete_from_json_file(filepath, key, value):
    data = read_json(filepath)
    if isinstance(data, list):
        data = [item for item in data if item.get(key) != value]
        write_json(filepath, data)

# Belirli bir öğeyi güncelle (liste içindeki sözlük)
def update_json_item(filepath, key, value, updated_item):
    data = read_json(filepath)
    if isinstance(data, list):
        for i, item in enumerate(data):
            if item.get(key) == value:
                data[i] = updated_item
                break
        write_json(filepath, data)

# Belirli öğeyi bul (tek eşleşme bekleniyorsa)
def find_in_json(filepath, key, value):
    data = read_json(filepath)
    if isinstance(data, list):
        for item in data:
            if item.get(key) == value:
                return item
    return None

# Tüm eşleşmeleri döndür (filtreleme)
def filter_json_items(filepath, key, value):
    data = read_json(filepath)
    if isinstance(data, list):
        return [item for item in data if item.get(key) == value]
    return []

    
