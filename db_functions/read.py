import datetime as dt

import cnx
import ui


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
def check_available_suppliers(cursor):
    """Print list of suppliers with corresponding products and contact details, return `None`"""
    cursor.execute("""SELECT suppliers.supplier_id, suppliers.name, products.name AS "supplies", contacts.email, contacts.phone_no 
                    FROM suppliers JOIN products_to_suppliers ON suppliers.supplier_id = products_to_suppliers.product_id 
                    JOIN products ON products.product_id = products_to_suppliers.product_id 
                    JOIN contacts ON contacts.contact_id = suppliers.contact_id""")
    records = list(dict(zip(cursor.column_names, fetch)) for fetch in cursor.fetchall())
    ui.print_title(f'List of suppliers with corresponding products and contact details:')
    for record in records:
        print(record)
    input('\nPress [Enter] to return to MENU')
    # TODO: Pretty printing


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
def is_midrate_up_to_date(cursor):
    """Check whether the dating in midrate table is today or not

    Returns
        True: If the date in midrate table is TODAY
        False: If the date in the midrate table is YESTERDAY
    """
    cursor.execute("SELECT date_updated FROM mid_exchange_rate LIMIT 1")
    try:
        if cursor.fetchall()[0][0] == dt.date.today():
            return True
        return False
    except IndexError:
        return False
