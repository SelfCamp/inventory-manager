# Az árfolyamokat a napiárfolyam.hu gyüjti

import datetime as dt
import itertools
import unittest
import xml.etree.ElementTree as ET

import requests

import cnx
import static_data


@cnx.connection_handler
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


@cnx.connection_handler
def is_midrate_up_to_date(cursor):
    """Check whether the dating in midrate table is today or not

    Returns
        True: If the date in midrate table is TODAY
        False: If the date in the midrate table is YESTERDAY
    """
    cursor.execute("SELECT date_updated FROM mid_exchange_rate LIMIT 1")
    try:
        if cursor.fetchall()[0][0] == dt.date.today():
            return True
        return False
    except IndexError:
        return False


@cnx.connection_handler
def sql_table_import(cursor, file, database):
    with open(file) as f:
        headers_list = str(*itertools.islice(f, 1)).strip().split(";")
        data_list = list(line.strip().split(";") for line in f)

    sql_query = f"INSERT INTO {database} ("
    for header in headers_list:
        sql_query += f"{header}, "
    sql_query = f"{sql_query[:-2]}) VALUES "

    for data in data_list:
        sql_query += "("
        for value in data:
            if value.isnumeric():
                sql_query += f"{value}, "
            else:
                sql_query += f"'{value}', "
        sql_query = f"{sql_query[:-2]}), "
    sql_query = sql_query[:-2]
    cursor.execute(sql_query)


@cnx.connection_handler
def fetch_table(cursor, database):
    cursor.execute(f"SELECT * FROM {database}")
    return cursor.fetchall()


@cnx.connection_handler
def sql_execute(cursor, statement):
    cursor.execute(statement)


class TestMidrate(unittest.TestCase):

    def setUp(self):
        midrate_updater()
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
                         set(static_data.CURRENCIES),
                         "Testing if required currencies are present")


class TestSQLTableImport(unittest.TestCase):

    def setUp(self):
        sql_execute("CREATE TABLE unittest (supplier_id INT NOT NULL AUTO_INCREMENT, "
                    "name VARCHAR(50) NOT NULL, contact_id INT NOT NULL, PRIMARY KEY (supplier_id));")
        sql_table_import("drafts/unittest_table.csv","unittest")
        with open("drafts/unittest_table.csv") as f:
            self._file = list(line.strip().split(";") for line in f)[1:]
        self._sql = fetch_table("unittest")
        self._trials = []
        for sql, file in zip(self._sql, self._file):
            self._trials.extend(list(str(subsql) == str(subfile) for subsql, subfile in zip(sql, file)))

    def test_import(self):
        self.assertTrue(all(self._trials),"Testing if data is correctly added to table")

    def tearDown(self):
        sql_execute("DROP TABLE unittest")


if __name__ == '__main__':
    unittest.main()
