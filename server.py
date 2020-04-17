import sqlite3
from database import *
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

queries = {
    'create_users_table': """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password_hash BLOB NOT NULL,
                                last_active INTEGER DEFAULT 0 NOT NULL 
                                );""",
    'create_messages_table': """CREATE TABLE IF NOT EXISTS messages (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                  text TEXT NOT NULL,
                                  time INTEGER NOT NULL, 
                                  user_id INTEGER NOT NULL, 
                                  FOREIGN KEY (user_id) REFERENCES users (id)
                                );""",
    'select_all_users': """SELECT * FROM users"""
}

connection = createConnection("data.sqlite3")
executeQuery(connection, queries['create_users_table'])
executeQuery(connection, queries['create_messages_table'])
connection.close()


@app.route("/")
def hello():
    return "<h1>My First Python Messenger</h1>"


@app.route("/status")
def status():
    """
    Print server status, time, users amount & messages amount

    request: -
    response: -
    """
    connection = createConnection("data.sqlite3")

    select_users_count = "SELECT Count(*) FROM users"
    users_count = executeReadQuery(connection, select_users_count, 0)

    select_messages_count = "SELECT Count(*) FROM messages"
    messages_count = executeReadQuery(connection, select_messages_count, 0)

    connection.close()
    return {
        "status": True,
        "time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "users_count": users_count[0],
        "messages_count": messages_count[0],
    }


@app.route("/messages")
def messagesView():
    """
    Receive messages after point "after"

    request: ?after=1234567890.4
    response: {
        "messages": [
            {"username": "str", "text": "str", "time": float},
            ...
        ]
    }
    """
    after = float(request.args['after'])
    new_messages = []

    connection = createConnection("data.sqlite3")

    select_messages = f"SELECT * FROM messages WHERE time > :after"
    query_data = executeReadQuery(connection, select_messages, 1, {'after': after})

    for item in query_data:
        select_username = f"SELECT username FROM users WHERE id LIKE :item"
        username = executeReadQuery(connection, select_username, 0, {'item': item[3]})
        message = {'username': username[0], 'text': item[1], 'time': item[2]}
        new_messages.append(message)

    connection.close()
    return {"messages": new_messages}


@app.route("/send", methods=['POST'])
def sendView():
    """
    Send message

    request: {
        "username": str,
        "text": str
    }
    response: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    text = data["text"]

    connection = createConnection("data.sqlite3")

    select_user_id = f"SELECT id FROM users WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_user_id, 0, {'username': username})

    data_dict = {'text': text, 'id': query_data[0]}
    new_message = f"INSERT INTO messages (text, time, user_id) " \
                  f"VALUES (:text, strftime('%s','now'), :id)"
    executeQuery(connection, new_message, data_dict)

    connection.close()
    return {'ok': True}


@app.route("/auth", methods=['POST'])
def authUser():
    """
    Authentificate User

    request: {
        "username": str,
        "password": str
    }
    response: {
        "exist": bool,
        "match": bool
    }
    """
    username = request.authorization.username
    password = request.authorization.password

    connection = createConnection("data.sqlite3")

    select_user_password = f"SELECT password_hash FROM users WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_user_password, 0, {'username': username})

    password_hash = codec(query_data[0], 0)

    if query_data is None:
        return {'exist': False, 'match': False}
    elif not checkPassword(password.encode(), password_hash):
        return {'exist': True, 'match': False}

    connection.close()
    return {'exist': True, 'match': True}


@app.route("/signup", methods=['POST'])
def signupUser():
    """
    Register User

    request: {
        "username": str,
        "password": str
    }
    response: {
        "loginOutOfRange": bool,
        "passwordOutOfRange": bool,
        "ok": bool
    }
    """
    username = request.authorization.username
    password = request.authorization.password

    if len(username) not in range(4, 20, 1):
        return {"loginOutOfRange": True}
    elif len(password) not in range(4, 20, 1):
        return {"loginOutOfRange": False, "passwordOutOfRange": True}

    connection = createConnection("data.sqlite3")

    select_user = f"SELECT * FROM users WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_user, 0, {'username': username})

    if query_data is None:
        password_hash = codec(password, 1)
        password_hash = sqlite3.Binary(password_hash)
        data_dict = {'username': username, 'password_hash': password_hash}
        create_user = f"INSERT INTO users (username, password_hash)" \
                      f"VALUES (:username, :password_hash)"
        executeQuery(connection, create_user, data_dict)
    else:
        return {"loginOutOfRange": False, "passwordOutOfRange": False, 'ok': False}

    connection.close()
    return {"loginOutOfRange": False, "passwordOutOfRange": False, 'ok': True}


app.run()
