# Az árfolyamokat a napiárfolyam.hu gyüjti

import static_data
import requests
import xml.etree.ElementTree as ET
import datetime as dt
import cnx
import itertools
import unittest

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


@cnx.connection_handler
def fetch_table(cursor, database):
    cursor.execute(f"SELECT * FROM {database}")
    return cursor.fetchall()


class TestMidrate(unittest.TestCase):

    def setUp(self):
        #midrate_updater()
        self._midrate_table = fetch_table("mid_exchange_rate")

    def test_number_of_records(self):
        self.assertEqual(len(self._midrate_table), 17, "Testing the number of expected records...")

    def test_up_to_date(self):
        self.assertTrue(all(date[1] == dt.date.today() for date in self._midrate_table),
                        "Testing if all records are up to date")

    def test_currency_id_length(self):
        currency_id_length = set(len(currency[0]) for currency in self._midrate_table)
        self.assertEqual(currency_id_length, {3, }, "Testing if currency length is 3")

    def test_currency_id_contents(self):
        self.assertEqual(set(element[0] for element in self._midrate_table),
                         set(static_data.currencies),
                         "Testing if required currencies are present")

if __name__ == '__main__':
    unittest.main()

