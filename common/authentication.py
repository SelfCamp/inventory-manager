import hashlib

from common import cnx
from common.general import quit_application


@cnx.connection_handler()
def authenticate(cursor, max_attempts=999):
    """Authenticate user, return `username` if authentication is successful, else `None`

    Args
        - `max_attempts=999` (optional): Max number of login attempts before the code terminates (999 by default)
    """
    num_of_attempts = 0
    while True:
        if num_of_attempts >= max_attempts:
            print("Too many failed login attempts")
            return None
        username = input("\nPlease enter your username or 'x' to quit: ")
        if username.lower() == "x":
            quit_application()
        password = hash_sha256(input("\nPlease enter your password: "))

        cursor.execute("SELECT password FROM users WHERE username = %(username)s", params={"username": username})
        try:
            password_in_db = cursor.fetchall()[0][0]
        except IndexError:
            print("Incorrect username or password")
            num_of_attempts += 1
            continue
        if password_in_db == password:
            return username
        else:
            print("Invalid username / password")
            num_of_attempts += 1
            continue


def hash_sha256(text):
    """Take `text` (integer or string) and return hashed string with sha256 encryption"""
    hash_object = hashlib.sha256(bytes(f"{text}".encode("utf8")))
    hex_dig = hash_object.hexdigest()
    return hex_dig
