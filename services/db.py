import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from config import DATABASE_CONNECTION_FILE

def get_credentials():
    """Read database credentials from JSON file."""
    try:
        with open(DATABASE_CONNECTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{DATABASE_CONNECTION_FILE} not found.")
    except json.JSONDecodeError:
        print(f"{DATABASE_CONNECTION_FILE} is not valid JSON.")
    except Exception as e:
        print(f"Error reading DB credentials: {e}")
    return None

def get_data_list(query, params=None):
    """Execute query and return all results as a list."""
    creds = get_credentials()
    if not creds:
        return []
    results = []
    try:
        with psycopg2.connect(**creds) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                results = cur.fetchall()
    except Exception as e:
        print("Database error:", e)
    return results

def get_data(query, params=None):
    """Execute query and return a single record."""
    creds = get_credentials()
    if not creds:
        return None
    result = None
    try:
        with psycopg2.connect(**creds) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                result = cur.fetchone()
    except Exception as e:
        print("Database error:", e)
    return result