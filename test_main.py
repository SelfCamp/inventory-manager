"""Database testing functionality with bells & whistles, completely separate from main app functionality"""


import mysql.connector
import cnx
import test_queries


def get_connection(remote):
    """Return `MySQL connection object`, connecting to one of two MySQL servers"""
    if remote:
        return mysql.connector.connect(**cnx.REMOTE)
    else:
        return mysql.connector.connect(**cnx.LOCAL)


def make_queries(queries, autocommit=False, remote=False, verbose=False):
    """Execute queries on one of two MySQL servers

    Args
        - `queries`: iterable with one or more separate SQL query strings

    Kwargs
        - `remote=True`: run on `REMOTE` server instead of `LOCAL`
        - `verbose=True`: print success rate and connection info to console (errors are always printed)
    """
    connection = get_connection(remote)
    connection.autocommit = autocommit
    cursor = connection.cursor()

    successful = 0
    for i, query in enumerate(queries):
        try:
            cursor.execute(query)
            connection.commit()
            successful += 1
        except Exception as err:
            print(f'ERROR {err}')
            if i < len(queries)-1:
                print('Continuing with other queries.\n')

    if verbose:
        print(f'Executed {successful} out of {len(queries)} queries successfully.')

    cursor.close()
    connection.close()
    if verbose:
        print('Connection closed.')


def main(autocommit=False, remote=False, verbose=False):
    make_queries([test_queries.drop, test_queries.create, test_queries.populate], autocommit, remote, verbose)


if __name__ == '__main__':
    main(autocommit=False, remote=False, verbose=True)
