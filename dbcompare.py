import mysql.connector
from mysql.connector import Error


def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            ssl_disabled=True
        )
        if connection.is_connected():
            print(f"Connected to {database}")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def get_table_names(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [table[0] for table in tables]


def get_table_schema(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"DESCRIBE {table_name}")
    schema = cursor.fetchall()
    return [col[0] for col in schema]  # Return only column names


def compare_schemas(schema1, schema2):
    return schema1 == schema2


def main():
    db1_config = {
        'host': '192.168.15.251',
        'user': 'db_user',
        'password': 'Dbuser@123',
        'database': 'mam_30042024'
    }

    db2_config = {
        'host': '192.168.15.245',
        'user': 'db_user',
        'password': 'Pmsltesting@1234',
        'database': 'mamcdb_mdmanager'
    }

    connection1 = connect_to_database(**db1_config)
    connection2 = connect_to_database(**db2_config)

    if not connection1 or not connection2:
        print("Error connecting to one or both databases.")
        return

    tables1 = get_table_names(connection1)
    tables2 = get_table_names(connection2)

    common_tables = set(tables1).intersection(set(tables2))

    for table in common_tables:
        schema1 = get_table_schema(connection1, table)
        schema2 = get_table_schema(connection2, table)

        if schema1 != schema2:
            print(f"Schema mismatch in table: {table}")

    connection1.close()
    connection2.close()


if __name__ == "__main__":
    main()
