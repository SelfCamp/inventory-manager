from classes.User import User
from common.authentication import authenticate
from common.general import quit_application
from menu_functions import admin_functions as af, read_functions as rf, update_functions as uf


def menu_handler(current_user):
    MENU = [
        {'description': 'Reset database',                      'fn': af.reset_database},
        {'description': 'Check complete inventory',            'fn': rf.get_inventory},
        {'description': 'Check stock level for product ID',    'fn': rf.get_stock_level_for_product_id},
        {'description': 'Request supplier information',        'fn': rf.get_available_suppliers},
        {'description': 'Check status of purchase order',      'fn': rf.get_po_status_for_po_id},
        {'description': 'Update stock level for inventory ID', 'fn': uf.set_stock_level_for_inventory_id},
        {'description': 'Quit application',                    'fn': quit_application}
    ]
    print('\nMENU')
    for num, item in enumerate(MENU):
        print(f"{num}: {item['description']}")
    choice = int(input('\nPlease type number of your choice: '))
    MENU[choice]['fn'](current_user)
    input('\nPress [Enter] to return to MENU')


def main():
    username = authenticate(max_attempts=2) or quit_application()
    current_user = User(username)
    uf.set_midrate()
    while True:
        menu_handler(current_user)


if __name__ == '__main__':
    main()
