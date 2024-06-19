import pymysql

# Database connection configurations
db1_config = {
    'host': '192.168.15.235',
    'user': 'db_user',
    'password': 'Pmsltesting@1234',
    'database': 'pamcdb_cloud'
}

db2_config = {
    'host': '192.168.15.245',
    'user': 'db_user',
    'password': 'Pmsltesting@1234',
    'database': 'mamcdb_mdmanager'
}


# Connect to the databases
def connect_to_db(config):
    return pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )


# Get table schemas
def get_table_schema(connection, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"DESCRIBE {table_name}")
        return {row[0]: row[1] for row in cursor.fetchall()}


# Compare schemas and print mismatches
def compare_schemas(db1_connection, db2_connection):
    with db1_connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        db1_tables = {row[0] for row in cursor.fetchall()}

    with db2_connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        db2_tables = {row[0] for row in cursor.fetchall()}

    common_tables = db1_tables.intersection(db2_tables)

    for table in common_tables:
        db1_schema = get_table_schema(db1_connection, table)
        db2_schema = get_table_schema(db2_connection, table)

        all_columns = set(db1_schema.keys()).union(set(db2_schema.keys()))

        for column in all_columns:
            db1_col_type = db1_schema.get(column)
            db2_col_type = db2_schema.get(column)

            if db1_col_type != db2_col_type:
                print(f"Table: {table}, Column: {column}")
                print(f"    Database 1 Type: {db1_col_type}")
                print(f"    Database 2 Type: {db2_col_type}")
            # else:
            #     print('not found ', column)


if __name__ == '__main__':
    db1_connection = connect_to_db(db1_config)
    db2_connection = connect_to_db(db2_config)

    compare_schemas(db1_connection, db2_connection)

    db1_connection.close()
    db2_connection.close()
