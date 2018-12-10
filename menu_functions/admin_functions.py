from common import cnx, constants
from common.csv_import import import_table_from_csv
from menu_functions import admin_queries as aq


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
    """Rebuild all tables from original schema, return `None`"""
    print("Rebuilding tables...", end='')
    for statement in aq.create_database_multi.strip('; \n\t').split(';'):  # TODO: consider making this a `common` function
        cursor.execute(statement)
    print(" DONE")


def mass_import_data():
    """Add data to tables based on .CSV files in `/starter_data`, return `None`"""
    for table, file in constants.STARTER_DATA_FILES.items():
        print(f'Importing to {table}...', end='')
        import_table_from_csv(file, table)
        print(f" DONE")


def reset_database():
    """Reset full database by dropping, rebuilding and importing data to tables"""
    drop_tables()
    rebuild_tables()
    mass_import_data()
    print("\nReset finished!")
