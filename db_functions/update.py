from xml.etree import ElementTree as ET
import datetime as dt
import requests

import cnx
from db_functions.read import is_midrate_up_to_date


@cnx.connection_handler()
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


@cnx.connection_handler()
def midrate_updater(cursor):
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
