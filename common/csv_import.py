import itertools

from common import cnx


@cnx.connection_handler()
def import_table_from_csv(cursor, file, database):
    with open(file, encoding="utf8") as f:
        headers_list = str(*itertools.islice(f, 1)).strip().split(";")
        data_list = list(line.strip().split(";") for line in f)

    sql_query = f"INSERT INTO {database} ("
    for header in headers_list:
        sql_query += f"{header}, "
    sql_query = f"{sql_query[:-2]}) VALUES "

    for data in data_list:
        sql_query += "("
        for value in data:
            if value.isnumeric() or value == 'NULL':
                sql_query += f"{value}, "
            else:
                sql_query += f"'{value}', "
        sql_query = f"{sql_query[:-2]}), "
    sql_query = sql_query[:-2]
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    cursor.execute(sql_query)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
