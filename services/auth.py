from typing import Optional
from models.user import User

def authenticate(username: str, password: str, users_db: list) -> Optional[User]:
    """
    Validates the given username and password against the users_db.
    If valid, returns a User instance; otherwise, returns None.
    users_db should be a list of lists: [[username, password, role], ...]
    """
    for user_record in users_db:
        if (
            len(user_record) >= 3 and
            user_record[0] == username and
            user_record[1] == password
        ):
            return User(
                username=user_record[0],
                email="",  # Or fill if you have email in user_record
                role=user_record[2]
            )
    return None