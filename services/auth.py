# auth.py
from collections import namedtuple

User = namedtuple("User", ["username", "role"])

def authenticate(input_username: str, input_password: str, row: tuple | None):
    if row is None:
        return None

    db_username, db_password, db_role = row
    if input_username == db_username and input_password == db_password:  # Gerekirse hash kontrolü ekleyin
        return User(username=db_username, role=db_role)
    return None