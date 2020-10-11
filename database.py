from sqlite3 import Error, connect


def createConnection(path):
    connection = None

    try:
        connection = connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def executeQuery(connection, query, data=None):
    cursor = connection.cursor()

    try:
        if data:
            cursor.execute(query, data)
            connection.commit()

        else:
            cursor.execute(query)
            connection.commit()

    except Error as e:
        print(f"The error '{e}' occurred")


def executeReadQuery(connection, query, flag=1, data=None):
    cursor = connection.cursor()
    result = None

    try:
        if data:
            cursor.execute(query, data)
            result = cursor.fetchall() if flag else cursor.fetchone()
            return result

        else:
            cursor.execute(query)
            result = cursor.fetchall() if flag else cursor.fetchone()
            return result

    except Error as e:
        print(f"The error '{e}' occurred")
