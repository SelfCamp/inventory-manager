import hashlib

from common import cnx


@cnx.connection_handler()
def authentication(cursor, max_attempts=999):
    """Authenticate user, return `True` if authentication is successful

    Args
        - `max_attempts=999` (optional): Max number of login attempts before the code terminates (999 by default)
    """
    num_of_attempts = 0
    while True:
        if num_of_attempts >= max_attempts:
            print("Too many failed login attempts")
            quit()
        user = input("Please enter your username or X to quit\n")
        if user.lower() == "x":
            quit()
        password = hash_sha256(input("Please enter your password\n"))

        cursor.execute("SELECT password FROM users WHERE username = '%(username)s'" % {"username": user})
        try:
            password_in_db = cursor.fetchall()[0][0]
        except IndexError:
            print("Incorrect username or password")
            num_of_attempts += 1
            continue
        if password_in_db == password:
            print(f"Welcome, {user}!\n")
            return True
        else:
            print("Invalid username / password")
            num_of_attempts += 1
            continue


def hash_sha256(text):
    """Take `text` (integer or string) and return hashed string with sha256 encryption"""

    hash_object = hashlib.sha256(bytes(f"{text}".encode("utf8")))
    hex_dig = hash_object.hexdigest()
    return hex_dig

