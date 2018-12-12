from xml.etree import ElementTree as ET
import datetime as dt
import requests

from common import cnx
from menu_functions.read_functions import is_midrate_up_to_date
from menu_functions import read_queries as rq, update_queries as uq


@cnx.connection_handler()
def set_stock_level_for_inventory_id(cursor):
    """Update stock level for a given inventory ID from user input"""
    inventory_id = input('\nPlease enter inventory ID: ')
    cursor.execute(rq.read_stock_level_for_inventory_id, params={'inventory_id': inventory_id})
    result = cursor.fetchall()
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'\nCurrent quantity of \'{name}\' at {loc} on rack {rack}, shelf {shelf} (expires on {exp}): {qty} {unit}')
    new_level = input('Please enter new quantity: ')
    cursor.execute(uq.update_stock_level_for_inventory_id, params={'new_level': new_level, 'inventory_id': inventory_id})
    cursor.execute(rq.read_stock_level_for_inventory_id, params={'inventory_id': inventory_id})
    result = cursor.fetchall()
    for loc, qty, exp, rack, shelf, name, unit in result:
        print(f'\nUpdated quantity of \'{name}\' at {loc} on rack {rack}, shelf {shelf} (expires on {exp}): {qty} {unit}')


@cnx.connection_handler()
def set_midrate(cursor):
    """Check if midrate table is up to date, if not, update table from napiarfolyam.hu"""

    if is_midrate_up_to_date():
        print("Foreign currency mid-rates are up to date!")
        return None

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
