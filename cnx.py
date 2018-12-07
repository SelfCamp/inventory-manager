import os
from functools import wraps

import mysql.connector


LOCAL = {
    'host':     os.environ.get('local_host'),
    'database': os.environ.get('local_database'),
    'user':     os.environ.get('local_user'),
    'password': os.environ.get('local_password')
}

REMOTE = {
    'host':     os.environ.get('remote_host'),
    'database': os.environ.get('remote_database'),
    'user':     os.environ.get('remote_user'),
    'password': os.environ.get('remote_password')
}


def get_connection(remote=True):
    """Return `MySQL connection object`, connecting to one of two MySQL servers

    Kwargs
        - `remote=False`: run on server configured as `REMOTE`
        - `remote=True`: run on server configured as `LOCAL`
    """
    if remote:
        return mysql.connector.connect(**REMOTE)
    else:
        return mysql.connector.connect(**LOCAL)


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
