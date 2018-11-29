import mysql.connector
import connection_data
import test_queries


def get_connection(remote):
    if remote:
        return mysql.connector.connect(**connection_data.REMOTE)
    else:
        return mysql.connector.connect(**connection_data.LOCAL)


def make_queries(queries, autocommit=False, remote=False, verbose=False):
    """Execute one or more separate SQL queries in `queries` on one of two database servers

    `remote=False`: will run on server configured as `LOCAL`
    `remote=True`: will run on server configured as `REMOTE`
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
