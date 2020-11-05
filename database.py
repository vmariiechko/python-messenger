from sqlite3 import Error, connect


def create_connection(path):
    connection = None

    try:
        connection = connect(path)
    except Error as error:
        print(f"The error '{error}' occurred")

    return connection


def execute_query(connection, query, data=None):
    cursor = connection.cursor()

    try:
        if data:
            cursor.execute(query, data)
            connection.commit()
            cursor.close()

        else:
            cursor.execute(query)
            connection.commit()
            cursor.close()

    except Error as error:
        print(f"The error '{error}' occurred")


def execute_read_query(connection, query, flag=1, data=None):
    cursor = connection.cursor()
    result = None

    try:
        if data:
            cursor.execute(query, data)
            result = cursor.fetchall() if flag else cursor.fetchone()
            cursor.close()
            return result

        else:
            cursor.execute(query)
            result = cursor.fetchall() if flag else cursor.fetchone()
            cursor.close()
            return result

    except Error as error:
        print(f"The error '{error}' occurred")
