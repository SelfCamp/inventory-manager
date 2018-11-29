import mysql.connector
import connection_data
import test_queries


def get_connection(remote):
    if remote:
        return mysql.connector.connect(**connection_data.REMOTE)
    else:
        return mysql.connector.connect(**connection_data.LOCAL)


def main(queries, autocommit=False, remote=False):
    """Execute each SQL query in `queries` on one of two database servers

    `remote=False`: will run on server configured as `LOCAL`
    `remote=True`: will run on server configured as `REMOTE`
    """
    connection = get_connection(remote)
    connection.autocommit = autocommit
    cursor = connection.cursor()

    successful = 0
    for query in queries:
        try:
            cursor.execute(query)
            connection.commit()
            successful += 1
        except Exception as err:
            print(f'Error: {err}\n       Continuing with other queries.')

    print(f'Executed {successful} out of {len(queries)} queries successfully.')

    connection.close()
    print('Connection closed.')


if __name__ == '__main__':
    main(
         queries=(
             test_queries.drop,
             test_queries.create,
             test_queries.populate
                 ),
         autocommit=False,
         remote=True
        )
