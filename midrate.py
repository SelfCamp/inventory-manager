# Az árfolyamokat a napiárfolyam.hu gyüjti

import requests
import xml.etree.ElementTree as ET
import datetime as dt
import cnx
import itertools

@cnx.connection_handler
def midrate_updater(cursor):
    """ Checks if midrate table is up to date. Updates table from napiarfolyam.hu if dates are in the past."""
    """
    if is_midrate_up_to_date():
        print("Foreign currency mid-rates are up to date!")
        return None
"""
    response = requests.get("http://api.napiarfolyam.hu/?bank=mnb")
    root = ET.fromstring(response.text)

    currency_list = list(currency.text for currency in root.findall("./deviza/item/penznem"))
    midrate_list = list(midrate.text for midrate in root.findall("./deviza/item/kozep")[::2])
    currency_rate_list = list(zip(currency_list, midrate_list))

    cursor.execute("DELETE FROM mid_exchange_rate")
    to_sql = "INSERT INTO mid_exchange_rate (currency_id, date_updated, midrate_to_huf) VALUES "
    for elem in currency_rate_list:
        to_sql += " ('{}','{}','{}'),".format(elem[0], dt.date.today(), elem[1])
    to_sql = to_sql[:-1]
    cursor.execute(to_sql)

@cnx.connection_handler
def is_midrate_up_to_date(cursor):
    """Checks whether the dating in midrate table is today or not.

    Returns:
        True: If the date in midrate table is TODAY
        False: If the date in the midrate table is YESTERDAY
    """
    cursor.execute("SELECT date_updated FROM mid_exchange_rate LIMIT 1")
    if cursor.fetchall()[0][0] == dt.date.today():
        return True
    return False

@cnx.connection_handler
def sql_table_import(cursor, file, database):
    with open(file) as f:
        headers_list = str(*itertools.islice(f, 1)).strip().split(";")
        data_list = list(line.strip().split(";") for line in f)

    sql_query = "INSERT INTO " + database + " ("
    for header in headers_list:
        sql_query += header + ", "
    sql_query = sql_query[:-2] + ") VALUES "

    for data in data_list:
        sql_query += "("
        for value in data:
            if value.isnumeric():
                sql_query += value + ", "
            else:
                sql_query += "'" + value + "', "
        sql_query =  sql_query[:-2] + "), "
    sql_query = sql_query[:-2]
    cursor.execute(sql_query)


if __name__ == '__main__':
    midrate_updater()

#TODO: inventory exp date: show only date, time is not needed
#TODO: Fix phone number for contacts



    # sql_table_import(r"drafts\access_levels_table.csv", "access_levels")
    # sql_table_import(r"drafts\employees_table.csv", "employees")
    # sql_table_import(r"drafts\locations_table.csv", "locations")
    # sql_table_import(r"drafts\contacts_table.csv", "contacts")
    # sql_table_import(r"drafts\users_table.csv", "users")
    # sql_table_import(r"drafts\purchase_order_contents_table.csv", "purchase_order_contents")
    # sql_table_import(r"drafts\purchase_orders_table.csv", "purchase_orders")
    # sql_table_import(r"drafts\suppliers_table.csv", "suppliers")
    # sql_table_import(r"drafts\products_to_suppliers_table.csv", "products_to_suppliers")
    # sql_table_import(r"drafts\menu_items_table.csv", "menu_items")
    # sql_table_import(r"drafts\products_table.csv", "products")
    # sql_table_import(r"drafts\inventory_table.csv", "inventory")
    # sql_table_import(r"drafts\proportions_table.csv", "proportions")
