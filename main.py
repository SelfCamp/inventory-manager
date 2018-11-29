import mysql.connector
import connection_data
import test_queries
from functools import wraps


def get_connection(remote=False):
    """Return `MySQL connection object`, connecting to one of two MySQL servers

    Kwargs
        - `remote=False`: run on server configured as `REMOTE`
        - `remote=True`: run on server configured as `LOCAL`
    """
    if remote:
        return mysql.connector.connect(**connection_data.REMOTE)
    else:
        return mysql.connector.connect(**connection_data.LOCAL)


def connection_handler(fn):
    """Set up database connection & cursor, call `fn` with cursor, close connection, return `fn` result"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        connection = get_connection()
        connection.autocommit = True
        cursor = connection.cursor()
        result = fn(cursor, *args, **kwargs)
        cursor.close()
        connection.close()
        return result
    return wrapper


@connection_handler
def test_suite(cursor):
    cursor.execute(test_queries.drop)
    cursor.execute(test_queries.create)
    cursor.execute(test_queries.populate)


def main(testing):
    if testing:
        test_suite()
    else:
        pass


if __name__ == '__main__':
    main(testing=True)
