import datetime as dt
from xml.etree import ElementTree as ET

import requests

from classes.Table import Table
from common import cnx
from menu_functions import read_queries as rq, read_functions as rf, update_queries as uq


@cnx.connection_handler()
def set_stock_level_for_inventory_id(cursor, current_user):
    """Update stock level for a given inventory ID from user input"""
    inventory_id = input('\nPlease enter inventory ID: ')

    print('Current quantity:')
    table = Table(rq.read_global_inventory_for_inventory_id, params={'inventory_id': inventory_id})
    print(table)

    new_level = input('Please enter new quantity: ')
    print("Updating quantity...", end='')
    cursor.execute(uq.update_stock_level_for_inventory_id, params={'new_level': new_level, 'inventory_id': inventory_id})
    print(' DONE')


@cnx.connection_handler()
def set_midrate(cursor):
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
def remove_inventory_for_menu_item_on_location(cursor, current_user):
    # get user request and see if it's doable
    menu_item_id = input('\nPlease enter menu item ID: ')
    location_id = current_user.location_id
    max_portions = rf.get_max_portions_for_menu_item_on_location(current_user, menu_item_id)
    portions_to_remove = int(input(f'Please enter number of portions to remove: '))
    while portions_to_remove > max_portions:
        portions_to_remove = int(input(f'Amount exceeds stock level, please enter smaller number: '))

    # get all inventory data required for calculations
    cursor.execute(
        rq.read_local_inventory_for_menu_item,
        params={"location_id": location_id, 'menu_item_id': menu_item_id}
    )
    inventory_extract = cursor.fetchall()

    # calculate quantities to remove for each product_id
    products_to_remove = {
        row['product_id']: (portions_to_remove * row['needed_per_portion'])
        for row in inventory_extract
    }

    # TODO: display planned changes to user, have them approved, or rollback connection

    menu_item_name = inventory_extract[0]['menu_item_name']
    print(f"Removing inventory for {portions_to_remove} portions of \"{menu_item_name}\"...", end='')
    for product_id, total_to_remove in products_to_remove.items():
        remove_fifo(cursor, current_user, product_id, total_to_remove, check_if_possible=False)
    print(' DONE')


@cnx.connection_handler(dictionary=True)
def remove_fifo(cursor, current_user, product_id, total_to_remove, check_if_possible=False):
    """Remove local inventory for product_id, oldest items first (as in FIFO)"""
    cursor.execute(
        rq.read_local_inventory_for_product_id,
        params={'location_id': current_user.location_id, 'product_id': product_id}
    )

    before = cursor.fetchall()
    before = [row for row in before if row['quantity'] != 0]  # TODO: do in query instead
    before.sort(key=lambda row: row['expiration_date'])       # TODO: do in query instead

    inventory_to_update = {}
    for row in before:
        inventory_id = row['inventory_id']
        old_quantity = row['quantity']
        if old_quantity >= total_to_remove:
            new_quantity = old_quantity - total_to_remove
            total_to_remove = 0
            inventory_to_update.update({inventory_id: new_quantity})
            break
        else:
            new_quantity = 0
            total_to_remove -= old_quantity
            inventory_to_update.update({inventory_id: new_quantity})

    update_statements = []
    for inventory_id, new_quantity in inventory_to_update.items():
        update_statements.append(f"""
            UPDATE inventory SET quantity = {new_quantity}
            WHERE inventory_id = {inventory_id}
        """)

    for statement in update_statements:
        cursor.execute(statement)
