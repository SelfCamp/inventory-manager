from db_functions import admin, read, update


def quit_application():
    print('\nGoodbye!\n')
    quit()


def menu_handler():
    MENU = [
        ('0: Reset database', admin.reset_database),
        ('1: Check complete inventory', read.get_inventory),
        ('2: Check stock level for product ID', read.get_stock_level_for_product_id),
        ('3: Update stock level for inventory ID', update.update_stock_level_for_inventory_id),
        ('4: Request supplier information', read.check_available_suppliers),
        ('5: Quit application', quit_application)
    ]
    print('\nMENU')
    for description, fn in MENU:
        print(description)
    choice = input('\nPlease type number of your choice: ')
    MENU[int(choice)][1]()


def main():
    while True:
        menu_handler()


if __name__ == '__main__':
    main()
