from os import path
from sqlite3 import Error, connect

from bcrypt import hashpw, checkpw, gensalt
from cryptography.fernet import Fernet


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


def codec(password, flag):
    if not path.exists('../key'):
        key = generateKey()
    else:
        with open('../key', 'rb') as file:
            key = file.read()

    cipher_suite = Fernet(key)

    if flag:
        encrypted_hash = cipher_suite.encrypt(hashPassword(password))
        return encrypted_hash
    else:
        decrypted_hash = cipher_suite.decrypt(password)
        return decrypted_hash


def generateKey():
    key = Fernet.generate_key()

    with open('../key', 'wb') as file:
        file.write(key)

    return key


def hashPassword(password):
    password_hash = hashpw(password.encode(), gensalt())
    return password_hash


def checkPassword(password, hashed):
    return checkpw(password, hashed)
