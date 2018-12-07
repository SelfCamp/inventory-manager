import itertools

import cnx
import static_data


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


def mass_import_data():
    """Add data to tables based on .CSV files in `/starter_data`, return `None`"""
    for table, file in static_data.STARTER_DATA_FILES.items():
        print(f'Importing to {table}...', end='')
        sql_table_import(file, table)
        print(f" DONE")
