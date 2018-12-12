from common.authentication import authentication
from menu_functions import admin_functions as af, read_functions as rf, update_functions as uf
from classes.User import User


def quit_application(current_user):
    print(f'\nGoodbye, {current_user.username}!\n')
    quit()


def menu_handler(current_user):
    MENU = [
        {'description': '0: Reset database',                      'fn': af.reset_database},
        {'description': '1: Check complete inventory',            'fn': rf.get_inventory},
        {'description': '2: Check stock level for product ID',    'fn': rf.get_stock_level_for_product_id},
        {'description': '3: Request supplier information',        'fn': rf.get_available_suppliers},
        {'description': '4: Check status of purchase order',      'fn': rf.get_po_status_for_po_id},
        {'description': '5: Update stock level for inventory ID', 'fn': uf.set_stock_level_for_inventory_id},
        {'description': '6: Quit application',                    'fn': quit_application}
    ]
    print('\nMENU')
    for item in MENU:
        print(item['description'])
    choice = int(input('\nPlease type number of your choice: '))
    MENU[choice]['fn'](current_user)
    input('\nPress [Enter] to return to MENU')


def main():
    username = authentication(2)
    current_user = User(username)
    uf.set_midrate()
    while True:
        menu_handler(current_user)


if __name__ == '__main__':
    main()
