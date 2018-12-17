from xml.etree import ElementTree as ET
import datetime as dt
import requests

from common import cnx
from menu_functions import read_queries as rq, read_functions as rf, update_queries as uq
from classes.Table import Table


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


# TODO ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓

@cnx.connection_handler()
def remove_inventory_for_menu_item_on_location(cursor, current_user):
    menu_item_id = input('\nPlease enter menu item ID: ')
    location_id = current_user.location_id
    max_portions, menu_item_name = rf.get_max_portions_for_menu_item_on_location(current_user, menu_item_id)
    portions = int(input(f'\nPlease enter number of portions to remove: '))
    while portions > max_portions:
        portions = int(input(f'\nAmount exceeds stock level, please enter smaller number: '))




    print('DONE')
