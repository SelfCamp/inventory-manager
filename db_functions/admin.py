import cnx
from db_functions.csv_import import mass_import_data
from queries.schema import SCHEMA


@cnx.connection_handler()
def list_all_tables(cursor):
    """Return currently active databases as `list`"""
    cursor.execute("SHOW TABLES")
    return list(table[0] for table in cursor.fetchall())


@cnx.connection_handler()
def drop_tables(cursor):
    """Delete all active tables, return `None`"""
    print("Dropping tables...", end='')
    tables = list_all_tables()
    for table in tables:
        cursor.execute(f"DROP TABLE {table}")
    print(" Whoops!")


@cnx.connection_handler()
def rebuild_tables(cursor):
    """Rebuild all tables from `/schema.py`, return `None`"""
    print("Rebuilding tables...", end='')
    for statement in SCHEMA.strip('; \n\t').split(';'):  # TODO: consider making this a `common` function
        cursor.execute(statement)
    print(" DONE")


def reset_database():
    """Reset full database by dropping, rebuilding and importing data to tables"""
    drop_tables()
    rebuild_tables()
    mass_import_data()
    print("\nReset finished!")
    input('\nPress [Enter] to return to MENU')
