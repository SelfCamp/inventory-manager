import datetime as dt

from common import cnx
import ui
from menu_functions import read_queries as rq
from classes.Table import Table
from time import sleep


@cnx.connection_handler()
def get_inventory(cursor, current_user):
    """Fancy-print complete inventory across all locations"""
    cursor.execute(rq.read_inventory)
    result = cursor.fetchall()
    ui.print_title('Complete inventory across all locations (ordered by item name, location, then expiration date):')
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'{name}: {qty} {unit} at {loc} on rack {rack}, shelf {shelf} (expires on {exp})')


@cnx.connection_handler()
def get_available_suppliers(cursor, current_user):
    """Print list of suppliers with corresponding products and contact details, return `None`"""
    cursor.execute(rq.read_available_suppliers)
    records = list(dict(zip(cursor.column_names, fetch)) for fetch in cursor.fetchall())
    ui.print_title(f'List of suppliers with corresponding products and contact details:')
    for record in records:
        print(record)
    # TODO: Pretty printing


@cnx.connection_handler()
def get_stock_level_for_product_id(cursor, current_user):
    """Print stock level for a given product ID from user input"""
    product_id = input('\nPlease enter product ID: ')
    cursor.execute(rq.read_stock_level_for_product_id, params={'product_id': product_id})
    result = cursor.fetchall()
    name = result[0][5]
    ui.print_title(f'Inventory of \'{name}\' across all locations (ordered by location, then expiration date):')
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'{qty} {unit} at {loc} on rack {rack}, shelf {shelf} (expires on {exp})')


@cnx.connection_handler(dictionary=True)
def get_po_status_for_po_id(cursor, current_user):
    """Print status of purchase order for a given PO ID from user input"""
    po_id = input('\nPlease enter PO ID: ')
    cursor.execute(rq.read_po_status_for_po_id, params={'po_id': po_id})
    ui.print_title(f'Report on purchase order #{po_id}:')
    result = cursor.fetchall()[0]
    report = [
        {'title': 'Status', 'data': result['po_status'].upper()},
        {'title': 'Supplier', 'data': result['supplier']},
        {'title': 'Date ordered', 'data': result['date_ordered']},
        {'title': 'ETA', 'data': result['date_eta']},
        {'title': 'Date arrived', 'data': result['date_arrived'] or "Not arrived yet"},
        {'title': 'Signee', 'data': result['signee'] or "Not signed yet"}
    ]
    ui.print_titled_list(report, omit_empty=False)



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


@cnx.connection_handler(dictionary=True)
def get_employee_data(cursor, username):
    """Get all user data except password for user from database. Return it as `dictionary`"""
    cursor.execute(rq.read_user_info, params={"username": username})
    return cursor.fetchall()[0]  # TODO: Error proofing, list flattening


def get_inventory_on_location(current_user):
    """Get and print inventory data for current user's location. Return `none`"""
    table = Table(rq.read_inventory_on_location, {"location_id": current_user.location_id})
    print(table)


@cnx.connection_handler(dictionary=True)
def get_inventory_for_menu_item_on_location(cursor, current_user):
    menu_item_id = input('\nPlease enter menu item ID: ')
    location_id = current_user.location_id

    cursor.execute(
        rq.read_max_portions_for_menu_item_on_location,
        params={'location_id': location_id, 'menu_item_id': menu_item_id})
    result = cursor.fetchall()
    print(f"\n{location_id} has ingredients for "
          f"{result[0]['can_make']} portions of \"{result[0]['menu_item_name']}\".")
    sleep(2)

    print(f"\nRelated inventory details, ordered by expiration date:")
    sleep(1)
    table = Table(
        rq.read_inventory_for_menu_item_on_location,
        params={"location_id": location_id, 'menu_item_id': menu_item_id})
    print(table)
    sleep(2)

    print(f"\nRelated stock levels per product:")
    sleep(1)
    table = Table(
        rq.read_max_portions_by_ingredient_for_menu_item_on_location,
        params={"location_id": location_id, 'menu_item_id': menu_item_id})
    print(table)
