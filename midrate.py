# Az árfolyamokat a napiárfolyam.hu gyüjti

import requests
import xml.etree.ElementTree as ET
import datetime as dt
from main import connection_handler

@connection_handler
def midrate_updater(cursor):
    """ Checks if midrate table is up to date. Updates table from napiarfolyam.hu if dates are in the past."""
    if is_midrate_up_to_date() == False:
        print("Foreign currency mid-rates are up to date!")
        return None

    response = requests.get("http://api.napiarfolyam.hu/?bank=mnb")
    root = ET.fromstring(response.text)

    currency_list = list(currency.text for currency in root.findall("./deviza/item/penznem"))
    midrate_list = list(midrate.text for i, midrate in enumerate(root.findall("./deviza/item/kozep")) if i % 2 == 0)

    currency_rate_list = list(zip(currency_list, midrate_list))

    cursor.execute("DELETE FROM mid_exchange_rate")

    for elem in currency_rate_list:
        cursor.execute("INSERT INTO mid_exchange_rate (currency_id, date_updated, midrate_to_huf)"
                       "VALUES ('{}','{}','{}')".format(elem[0], dt.date.today(), elem[1]))


@connection_handler
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

if __name__ == '__main__':
    midrate_updater()