import cnx
from db_functions.csv_import import mass_import_data


@cnx.connection_handler
def list_all_tables(cursor):
    """Return currently active databases as `list`"""
    cursor.execute("SHOW TABLES")
    return list(table[0] for table in cursor.fetchall())


@cnx.connection_handler
def drop_tables(cursor):
    """Delete all active tables, return `None`"""
    print("Dropping tables...", end='')
    tables = list_all_tables()
    sql_statement = ""
    for table in tables:
        sql_statement += f"DROP TABLE {table};"
    try:
        cursor.execute(sql_statement)
    except:
        pass
    print(" Whoops!")


@cnx.connection_handler
def rebuild_tables(cursor):
    """Rebuild all tables from `/schema.sql`, return `None`"""
    print("Rebuilding tables...", end='')
    sql_statement = ""
    with open("queries/schema.sql") as f:
        sql_statement += f.read()
    try:
        cursor.execute(sql_statement)
    except:
        pass
    print(" DONE")


def reset_database():
    """Reset full database by dropping, rebuilding and importing data to tables"""
    drop_tables()
    rebuild_tables()
    mass_import_data()
    print("\nReset finished!")
    input('\nPress [Enter] to return to MENU')
