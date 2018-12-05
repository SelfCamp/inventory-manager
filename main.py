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
    """Function to list currently active databases.

    Returns:
        List of database names
    """
    cursor.execute("SHOW TABLES")
    return list(table[0] for table in cursor.fetchall())

@cnx.connection_handler
def drop_tables(cursor):
    """Deletes all active tables, returns none"""
    print("Dropping tables...", end='')
    tables = list_all_databases()
    sql_statement = ""
    for table in tables:
        sql_statement += f"DROP TABLE {table};"
    try:
        cursor.execute(sql_statement)
    except:
        pass
    print(" Whoops!")


@cnx.connection_handler
def rebuild_tables(cursor):
    """Rebuilds all tables from pizza_db.sql. Returns none."""
    print("Rebuilding tables...", end='')
    sql_statement = ""
    with open("pizza_db.sql") as f:
        sql_statement += f.read()
    try:
        cursor.execute(sql_statement)
    except:
        pass
    print(" DONE")

def mass_import_data():
    """This function adds data to tables based on .CSV files in /drafts. Returns none. """
    for table, file in static_data.database_dict.items():
        print(f'Importing to {table}...', end='')
        midrate.sql_table_import(file,table)
        print(f" DONE")

def reset_database():
    """This function does a full database reset by dropping, rebuilding and importing data to tables."""
    drop_tables()
    rebuild_tables()
    mass_import_data()
    print("\nReset finished!")


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

@cnx.connection_handler
def check_available_suppliers(cursor):
    cursor.execute("""SELECT suppliers.supplier_id, suppliers.name, products.name AS "supplies", contacts.email, contacts.phone_no 
                    FROM suppliers JOIN products_to_suppliers ON suppliers.supplier_id = products_to_suppliers.product_id 
                    JOIN products ON products.product_id = products_to_suppliers.product_id 
                    JOIN contacts ON contacts.contact_id = suppliers.contact_id""")
    records = list(dict(zip(cursor.column_names, fetch)) for fetch in cursor.fetchall())
    for record in records:
        print(record)

    #TODO: Pretty printing

def quit_application():
    print('\nGoodbye!\n')
    quit()


def menu_handler():
    MENU = [
        ('0: Reset database', reset_database),
        ('1: Check complete inventory', get_inventory),
        ('2: Check stock level by product ID', get_stock_level_for_product_id),
        ('3: Update stock level by inventory ID', update_stock_level_for_inventory_id),
        ('4: Request supplier information', check_available_suppliers),
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
