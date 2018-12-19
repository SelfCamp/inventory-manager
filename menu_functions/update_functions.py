import datetime as dt
from xml.etree import ElementTree as ET

import requests

from classes.Table import Table
from classes.LowStockError import LowStockError
from common import cnx
from menu_functions import read_queries as rq, read_functions as rf, update_queries as uq


@cnx.connection_handler()
def set_stock_level_for_inventory_id(connection, cursor, current_user):
    """Update stock level for a given inventory ID from user input"""
    inventory_id = input('\nPlease enter inventory ID: ')

    print('Current quantity:')
    table = Table(rq.read_global_inventory_for_inventory_id, params={'inventory_id': inventory_id})
    print(table)

    new_quantity = input('Please enter new quantity: ')
    print("Updating quantity...", end='')
    cursor.execute(
        uq.update_quantity_for_inventory_id,
        params={'new_quantity': new_quantity, 'inventory_id': inventory_id}
    )
    print(' DONE')


@cnx.connection_handler()
def set_midrate(connection, cursor):
    """Update midrate table from napiarfolyam.hu"""
    print("Updating foreign currency mid-rates...", end='')
    response = requests.get("http://api.napiarfolyam.hu/?bank=mnb")
    root = ET.fromstring(response.text)

    currency_list = list(currency.text for currency in root.findall("./deviza/item/penznem"))
    midrate_list = list(midrate.text for midrate in root.findall("./deviza/item/kozep")[::2])
    currency_rate_list = list(zip(currency_list, midrate_list))

    cursor.execute("DELETE FROM mid_exchange_rate")
    to_sql = "INSERT INTO mid_exchange_rate (currency_id, date_updated, midrate_to_huf) VALUES "
    for elem in currency_rate_list:
        to_sql += f" ('{elem[0]}','{dt.date.today()}','{elem[1]}'),"
    to_sql = to_sql[:-1]
    cursor.execute(to_sql)
    print(' DONE')


@cnx.connection_handler(dictionary=True)
def fifo_remove_products_for_menu_item(connection, cursor, current_user):
    """Remove local inventory for all ingredients of menu item, oldest items first (as in FIFO)"""
    menu_item_id = int(input('\nPlease enter menu item ID: '))
    location_id = current_user.location_id
    max_portions = rf.get_max_portions_for_menu_item_on_location(current_user, menu_item_id)
    portions_to_remove = int(input(f'Please enter number of portions to remove: '))
    while portions_to_remove > max_portions:
        portions_to_remove = int(input(f'Amount exceeds stock level, please enter smaller number: '))
    if portions_to_remove <= 0:
        return None

    cursor.execute(
        rq.read_local_inventory_for_menu_item,
        params={"location_id": location_id, 'menu_item_id': menu_item_id}
    )
    starting_inventory = cursor.fetchall()

    products_to_remove = {
        row['product_id']: (portions_to_remove * row['needed_per_portion'])
        for row in starting_inventory
    }

    # TODO: display planned changes to user, have them approved, or rollback connection
    menu_item_name = starting_inventory[0]['menu_item_name']
    print(f"Removing inventory for {portions_to_remove} portions of \"{menu_item_name}\"...", end='')
    for product_id, total_to_remove in products_to_remove.items():
        fifo_remove_product(connection, cursor, location_id, product_id, total_to_remove, check_if_possible=False)
    print(' DONE')


@cnx.connection_handler(dictionary=True)
def fifo_remove_product_ui_layer(connection, cursor, current_user):
    location_id = current_user.location_id
    product_id = int(input('\nPlease enter product ID: '))
    total_to_remove = int(input(f'\nPlease enter amount to remove: '))

    result = 'TBD'
    while result == 'TBD':
        try:
            result = fifo_remove_product(connection, cursor, location_id, product_id, total_to_remove, check_if_possible=True)
        except LowStockError:
            total_to_remove = int(input(f'Amount exceeds stock level, please enter smaller number: '))


def fifo_remove_product(connection, cursor, location_id, product_id, total_to_remove, check_if_possible=True):
    """Remove local inventory for product_id, oldest items first (as in FIFO)"""
    cursor.execute(
        rq.read_local_inventory_for_product_id,
        params={'location_id': location_id, 'product_id': product_id}
    )
    starting_inventory = cursor.fetchall()
    starting_inventory = [row for row in starting_inventory if row['quantity'] != 0]  # TODO: filter in query instead

    if check_if_possible:
        total_available = sum(row['quantity'] for row in starting_inventory)
        if total_to_remove > total_available:
            raise LowStockError

    inventory_to_update = {}
    for row in starting_inventory:
        inventory_id = row['inventory_id']
        old_quantity = row['quantity']
        if old_quantity >= total_to_remove:
            new_quantity = old_quantity - total_to_remove
            inventory_to_update.update({inventory_id: new_quantity})
            break
        else:
            new_quantity = 0
            total_to_remove -= old_quantity
            inventory_to_update.update({inventory_id: new_quantity})

    for inventory_id, new_quantity in inventory_to_update.items():
        cursor.execute(
            uq.update_quantity_for_inventory_id,
            params={'inventory_id': inventory_id, 'new_quantity': new_quantity}
        )
