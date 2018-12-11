import datetime as dt
import unittest
from common import authentication

from common import cnx, constants
from common.csv_import import import_table_from_csv
from menu_functions.update_functions import set_midrate


@cnx.connection_handler()
def fetch_table(cursor, table):
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()


@cnx.connection_handler()
def sql_execute(cursor, statement):
    cursor.execute(statement)


class TestMidrate(unittest.TestCase):

    def setUp(self):
        set_midrate()
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
                         set(constants.CURRENCIES),
                         "Testing if required currencies are present")


class TestSQLTableImport(unittest.TestCase):

    def setUp(self):
        sql_execute("CREATE TABLE unittest (supplier_id INT NOT NULL AUTO_INCREMENT, "
                    "name VARCHAR(50) NOT NULL, contact_id INT NOT NULL, PRIMARY KEY (supplier_id));")
        import_table_from_csv("starter_data/unittest_table.csv", "unittest")
        with open("starter_data/unittest_table.csv") as f:
            self._file = list(line.strip().split(";") for line in f)[1:]
        self._sql = fetch_table("unittest")
        self._trials = []
        for sql, file in zip(self._sql, self._file):
            self._trials.extend(list(str(subsql) == str(subfile) for subsql, subfile in zip(sql, file)))

    def test_import(self):
        self.assertTrue(all(self._trials),"Testing if data is correctly added to table")

    def tearDown(self):
        sql_execute("DROP TABLE unittest")


class TestHashSha256(unittest.TestCase):

    def test_hashing(self):
        self.assertEqual(authentication.hash_sha256(
            "Teljes összhangban kell szinkronba hozni a hatékony ágazatközi munkamegosztást."),
            "cd25b84ac3b573244bfc8b2fba257e244da3cd26b1718fb433c3620b733e7723",
            "Testing hash generation")

if __name__ == '__main__':
    unittest.main()
