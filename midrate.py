# Az árfolyamokat a napiárfolyam.hu gyüjti

import mysql.connector
import requests
import xml.etree.ElementTree as ET
import datetime as dt
from main import connection_handler

@connection_handler
def midrate_updater(cursor):

    cursor.execute("SELECT date_updated FROM mid_exchange_rate LIMIT 1")
    if cursor.fetchall()[0][0] == dt.date.today(): return None

    response = requests.get("http://api.napiarfolyam.hu/?bank=mnb")
    root = ET.fromstring(response.text)

    currency_list = []
    midrate_list = []

    for currency in root.findall("./deviza/item/penznem"):
        currency_list.append(currency.text)

    for midrate in root.findall("./deviza/item/kozep"):
        midrate_list.append(midrate.text)

    del midrate_list[::2]

    currency_rate_list = list(zip(currency_list, midrate_list))

    cursor.execute("DELETE FROM mid_exchange_rate")

    for elem in currency_rate_list:
        print(elem[0], dt.date.today(), elem[1])
        cursor.execute("INSERT INTO mid_exchange_rate (currency_id, date_updated, midrate_to_huf)"
                       "VALUES ('{}','{}','{}')".format(elem[0], dt.date.today(), elem[1]))

    cursor.execute("SELECT * FROM access_levels;")
    result = cursor.fetchall()
    print(result)

"""