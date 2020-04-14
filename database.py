import sqlite3
from sqlite3 import Error


def createConnection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def executeReadQuery(connection, query, flag):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall() if flag else cursor.fetchone()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
