import cnx
import test_queries


@cnx.connection_handler
def test_suite(cursor):
    cursor.execute(test_queries.drop)
    cursor.execute(test_queries.create)
    cursor.execute(test_queries.populate)
    cursor.execute(test_queries.select_by_salary)
    top_earners = cursor.fetchall()
    print('Employees who earn over 850 000 HUF/month:')
    for employee_id, first_name, last_name, contact_id, location_id, status, department, role, salary_huf in top_earners:
        print(f'- {first_name} {last_name} ({role} in {department}) earns {salary_huf} HUF')


@cnx.connection_handler
def reset_database(cursor):
    print('→ This will reset database when the feature is implemented')
    input('Press [Enter] to return to MENU')


@cnx.connection_handler
def get_inventory(cursor):
    print('→ This will check complete inventory when the feature is implemented')
    input('Press [Enter] to return to MENU')


@cnx.connection_handler
def get_stock_level_by_product_id(cursor):
    print('→ This will check stock level by product ID when the feature is implemented')
    input('Press [Enter] to return to MENU')


@cnx.connection_handler
def update_stock_level_by_inventory_id(cursor):
    print('→ This will update stock level by inventory ID when the feature is implemented')
    input('Press [Enter] to return to MENU')


def quit_application():
    print('\nGoodbye!\n')
    quit()


def menu_handler():
    MENU = [
        ('0: Reset database', reset_database),
        ('1: Check complete inventory', get_inventory),
        ('2: Check stock level by product ID', get_stock_level_by_product_id),
        ('3: Update stock level by inventory ID', update_stock_level_by_inventory_id),
        ('4: Quit application', quit_application)
    ]
    print('\nMENU')
    for description, fn in MENU:
        print(description)
    choice = input('\nPlease type number of your choice: ')
    MENU[int(choice)][1]()


def main(testing):
    if testing:
        test_suite()
    else:
        while True:
            menu_handler()


if __name__ == '__main__':
    main(testing=False)
