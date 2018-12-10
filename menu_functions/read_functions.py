import datetime as dt

import cnx
import ui
from menu_functions import read_queries as rq


@cnx.connection_handler()
def get_inventory(cursor):
    """Fancy-print complete inventory across all locations"""
    cursor.execute(rq.read_inventory)
    result = cursor.fetchall()
    ui.print_title('Complete inventory across all locations (ordered by item name, location, then expiration date):')
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'{name}: {qty} {unit} at {loc} on rack {rack}, shelf {shelf} (expires on {exp})')


@cnx.connection_handler()
def get_available_suppliers(cursor):
    """Print list of suppliers with corresponding products and contact details, return `None`"""
    cursor.execute(rq.read_available_suppliers)
    records = list(dict(zip(cursor.column_names, fetch)) for fetch in cursor.fetchall())
    ui.print_title(f'List of suppliers with corresponding products and contact details:')
    for record in records:
        print(record)
    # TODO: Pretty printing


@cnx.connection_handler()
def get_stock_level_for_product_id(cursor):
    """Print stock level for a given product ID from user input"""
    product_id = input('\nPlease enter product ID: ')
    cursor.execute(rq.read_stock_level_for_product_id, {'product_id': product_id})
    result = cursor.fetchall()
    name = result[0][5]
    ui.print_title(f'Inventory of \'{name}\' across all locations (ordered by location, then expiration date):')
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'{qty} {unit} at {loc} on rack {rack}, shelf {shelf} (expires on {exp})')


@cnx.connection_handler()
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
