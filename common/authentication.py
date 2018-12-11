import hashlib

from common import cnx


@cnx.connection_handler()
def authentication(cursor, max_attempts=999):
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
        if password_in_db.lower() == password:
            print(f"Welcome, {user}!\n")
            break
        else:
            print("Invalid username / password")
            num_of_attempts += 1
            continue


def hash_sha256(string):
    hash_object = hashlib.sha256(bytes(f"{string}".encode("utf8")))
    hex_dig = hash_object.hexdigest()
    return hex_dig
