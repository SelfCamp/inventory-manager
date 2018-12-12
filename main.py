from common.authentication import authentication
from menu_functions import admin_functions as af, read_functions as rf, update_functions as uf
from classes.User import User


def quit_application(current_user):
    print(f'\nGoodbye {current_user.username}!\n')
    quit()


def menu_handler(current_user):
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
    MENU[int(choice)][1](current_user)
    input('\nPress [Enter] to return to MENU')


def main():
    username = authentication(2)
    current_user = User(username)
    uf.set_midrate()
    while True:
        menu_handler(current_user)


if __name__ == '__main__':
    main()
