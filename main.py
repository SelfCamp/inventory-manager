import cnx
import midrate
import test_queries
import ui
import static_data

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
def list_all_databases(cursor):
    cursor.execute("SHOW TABLES")
    return list(table[0] for table in cursor.fetchall())

@cnx.connection_handler
def drop_tables(cursor):
    tables = list_all_databases()
    sql_statement = ""
    for table in tables:
        sql_statement += f"DROP TABLE {table};"
    cursor.execute(sql_statement)

@cnx.connection_handler
def rebuild_tables(cursor):
    sql_statement = ""
    with open("pizza_db.sql") as f:
        sql_statement += f.read()
    cursor.execute(sql_statement)

@cnx.connection_handler
def mass_import_data(cursor):
    pass

@cnx.connection_handler
def reset_database(cursor):
    database_dict = {"inventory": r"drafts/inventory_table.csv",
                     "locations": r"drafts/locations_table.csv",
                     "products": r"drafts/products_table.csv",
                     "products_to_suppliers": r"drafts/products_to_suppliers_table.csv",
                     "menu_items": r"drafts/menu_items_table.csv",
                     "proportions": r"drafts/proportions_table.csv",
                     "suppliers": r"drafts/suppliers_table.csv",
                     "contacts": r"drafts/contacts_table.csv",
                     "users": r"drafts/users_table.csv",
                     "purchase_orders": r"drafts/purchase_orders_table.csv",
                     "purchase_order_contents": r"drafts/purchase_order_contents_table.csv",
                     "access_levels": r"drafts/access_levels_table.csv",
                     "employees": r"drafts/employees_table.csv"
                     }

    print("Dropping tables. Oops!)


    sql_statement = "DROP TABLE mid_exchange_rate;"
    for table in database_dict.keys():
        sql_statement += f"DROP TABLE {table};"
    with open("pizza_db.sql") as f:
        sql_statement += f.read()
    cursor.execute(sql_statement, multi=True)
    for database, file in database_dict.items():
        midrate.sql_table_import(file,database)

    #TODO: Dynamic table drop



@cnx.connection_handler
def get_inventory(cursor):
    """Fancy-print complete inventory across all locations"""
    cursor.execute("""
        SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
               prod.name, prod.unit
        FROM inventory inv JOIN products prod
        ON inv.product_id = prod.product_id
        ORDER BY prod.name, inv.location_id, inv.expiration_date;
    """)
    result = cursor.fetchall()
    ui.print_title('Complete inventory across all locations (ordered by item name, location, then expiration date):')
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'{name}: {qty} {unit} at {loc} on rack {rack}, shelf {shelf} (expires on {exp})')
    input('\nPress [Enter] to return to MENU')


@cnx.connection_handler
def get_stock_level_for_product_id(cursor):
    """Print stock level for a given product ID from user input"""
    product_id = input('\nPlease enter product ID: ')
    cursor.execute(f"""
        SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
               prod.name, prod.unit
        FROM inventory inv JOIN products prod
        ON inv.product_id = prod.product_id
        WHERE prod.product_id = {product_id}
        ORDER BY inv.location_id, inv.expiration_date;
    """)
    result = cursor.fetchall()
    name = result[0][5]
    ui.print_title(f'Inventory of \'{name}\' across all locations (ordered by location, then expiration date):')
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'{qty} {unit} at {loc} on rack {rack}, shelf {shelf} (expires on {exp})')
    input('\nPress [Enter] to return to MENU')


@cnx.connection_handler
def update_stock_level_for_inventory_id(cursor):
    """Update stock level for a given inventory ID from user input"""
    inventory_id = input('\nPlease enter inventory ID: ')
    cursor.execute(f"""
        SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
               prod.name, prod.unit
        FROM inventory inv JOIN products prod
        ON inv.product_id = prod.product_id
        WHERE inv.inventory_id = {inventory_id}
    """)
    result = cursor.fetchall()
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'\nCurrent quantity of \'{name}\' at {loc} on rack {rack}, shelf {shelf} (expires on {exp}): {qty} {unit}')
    new_level = input('Please enter new quantity: ')
    cursor.execute(f"""
        UPDATE inventory SET quantity = {new_level}
        WHERE inventory_id = {inventory_id}
    """)
    cursor.execute(f"""
        SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
               prod.name, prod.unit
        FROM inventory inv JOIN products prod
        ON inv.product_id = prod.product_id
        WHERE inv.inventory_id = {inventory_id}
    """)
    result = cursor.fetchall()
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'\nUpdated quantity of \'{name}\' at {loc} on rack {rack}, shelf {shelf} (expires on {exp}): {qty} {unit}')
    input('Press [Enter] to return to MENU')


def quit_application():
    print('\nGoodbye!\n')
    quit()


def menu_handler():
    MENU = [
        ('0: Reset database', reset_database),
        ('1: Check complete inventory', get_inventory),
        ('2: Check stock level by product ID', get_stock_level_for_product_id),
        ('3: Update stock level by inventory ID', update_stock_level_for_inventory_id),
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
