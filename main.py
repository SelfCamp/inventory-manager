from menu_functions import admin_functions as af, read_functions as rf, update_functions as uf
import hashlib
from common import cnx


def quit_application():
    print('\nGoodbye!\n')
    quit()


def menu_handler():
    MENU = [
        ('0: Reset database', af.reset_database),
        ('1: Check complete inventory', rf.get_inventory),
        ('2: Check stock level for product ID', rf.get_stock_level_for_product_id),
        ('3: Request supplier information', rf.get_available_suppliers),
        ('4: Check status of purchase order', rf.get_po_status_for_po_id),
        ('5: Update stock level for inventory ID', uf.set_stock_level_for_inventory_id),
        ('6: Quit application', quit_application)
    ]
    print('\nMENU')
    for description, fn in MENU:
        print(description)
    choice = input('\nPlease type number of your choice: ')
    MENU[int(choice)][1]()
    input('\nPress [Enter] to return to MENU')


@cnx.connection_handler()
def authentication(cursor, max_attempts = 999):
    num_of_attempts = 0
    while True:
        if num_of_attempts >= max_attempts:
            print("Too many failed login attempts")
            quit()
        user = input("Please enter your username or X to quit\n")
        if user.lower() == "x": quit()
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


def main():
    authentication(2)
    while True:
        menu_handler()


if __name__ == '__main__':
    main()
