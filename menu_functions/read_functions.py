import datetime as dt

from common import cnx
import ui
from menu_functions import read_queries as rq
from classes.Table import Table


def get_global_inventory(current_user):
    table = Table(rq.read_global_inventory)
    print(table)


def get_local_inventory(current_user):
    location_id = current_user.location_id
    table = Table(rq.read_local_inventory, params={'location_id': location_id})
    print(table)


def get_available_suppliers(current_user):
    """Print list of suppliers with corresponding products and contact details, return `None`"""
    table = Table(rq.read_available_suppliers)
    print(table)


def get_global_stock_level_for_product_id(current_user):
    """Print stock level for a given product ID from user input"""
    product_id = input('\nPlease enter product ID: ')
    table = Table(rq.read_global_stock_level_for_product_id, params={'product_id': product_id})
    print(table)


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
    print('\nChecking if foreign currency mid-rates are up to date...', end='')
    cursor.execute("SELECT date_updated FROM mid_exchange_rate LIMIT 1")
    try:
        if cursor.fetchall()[0][0] == dt.date.today():
            print(' OK')
            return True
        print(' NO')
        return False
    except IndexError:
        print(' NO')
        return False


@cnx.connection_handler(dictionary=True)
def get_employee_data(cursor, username):
    """Get all user data except password for user from database, return it as `dict`"""
    cursor.execute(rq.read_user_info, params={"username": username})
    return cursor.fetchall()[0]  # TODO: Error proofing, list flattening


@cnx.connection_handler(dictionary=True)
def get_max_portions_for_menu_item_on_location(cursor, current_user, menu_item_id=None):
    menu_item_id = menu_item_id or input('\nPlease enter menu item ID: ')
    location_id = current_user.location_id

    cursor.execute(
        rq.read_local_max_portions_for_menu_item,
        params={'location_id': location_id, 'menu_item_id': menu_item_id}
    )
    result = cursor.fetchall()
    max_portions = result[0]['can_make']
    menu_item_name = result[0]['menu_item_name']
    print(f"\n{location_id} has ingredients for {max_portions} portions of \"{menu_item_name}\".")
    return max_portions, menu_item_name


def get_ingredient_levels_for_menu_item_on_location(current_user):
    menu_item_id = input('\nPlease enter menu item ID: ')
    location_id = current_user.location_id

    table = Table(
        rq.read_local_max_portions_by_ingredient_for_menu_item,
        params={"location_id": location_id, 'menu_item_id': menu_item_id})
    print(table)


def get_inventory_for_menu_item_on_location(current_user):
    menu_item_id = input('\nPlease enter menu item ID: ')
    location_id = current_user.location_id

    table = Table(
        rq.read_local_inventory_for_menu_item,
        params={"location_id": location_id, 'menu_item_id': menu_item_id})
    print(table)
