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
                                role INTEGER DEFAULT 1 NOT NULL,
                                registered INTEGER NOT NULL,
                                is_banned INTEGER DEFAULT 0,
                                is_active INTEGER DEFAULT 1 NOT NULL,
                                last_active INTEGER DEFAULT 0 NOT NULL 
                                );""",
    'create_messages_table': """CREATE TABLE IF NOT EXISTS messages (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                  text TEXT NOT NULL,
                                  time INTEGER NOT NULL, 
                                  user_id INTEGER NOT NULL, 
                                  FOREIGN KEY (user_id) REFERENCES users (id)
                                );""",
    'select_all_users': """SELECT * FROM users""",
    'select_all_usernames': """SELECT username FROM users""",
    'select_active_users': """SELECT username FROM users WHERE is_active = 1"""
}

user_server_commands = [
    {'name': 'help', 'description': 'List available commands'},
    {'name': 'myself', 'description': 'Show information about you'},
    {'name': 'online', 'description': 'Show all online users'},
    {'name': 'status', 'description': 'Show server status'},
    {'name': 'registered', 'description': 'List all registered users'},
]
admin_server_commands = [
    {'name': 'clear', 'description': 'Clear chat messages'},
    {'name': 'role', 'description': 'Change role of user'},
    {'name': 'ban', 'description': 'Ban user'},
    {'name': 'unban', 'description': 'Unban user'},
]

connection = createConnection("data.sqlite3")
executeQuery(connection, queries['create_users_table'])
executeQuery(connection, queries['create_messages_table'])
connection.close()


def help(username, args=None):  # Import all commands to special file
    # TODO check role for admin commands
    return user_server_commands + admin_server_commands


def online(username, args=None):
    connection = createConnection("data.sqlite3")

    if args:
        select_users = f"SELECT username, is_active, last_active " \
                       f"FROM users " \
                       f"WHERE username IN ({','.join(['?'] * len(args))})"
        query_data = executeReadQuery(connection, select_users, 1, args)
    else:
        query_data = executeReadQuery(connection, queries['select_active_users'])

    connection.close()
    return query_data


def myself(username, args=None):
    connection = createConnection("data.sqlite3")

    reg_date = f"SELECT id, role, registered, last_active " \
               f"FROM users " \
               f"WHERE username LIKE :username"
    query_data = executeReadQuery(connection, reg_date, 0, {'username': username})

    connection.close()
    return query_data


def registered(username, args=None):
    connection = createConnection("data.sqlite3")

    all_usernames = queries['select_all_usernames']
    query_data = executeReadQuery(connection, all_usernames)

    connection.close()
    return query_data


@app.route("/")
def hello():
    return "<h1>My First Python Messenger</h1>"


@app.route("/status")
def status(username=None, args=None):
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
def messagesHistory():
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

    select_messages = f"SELECT m.text, m.time, u.username FROM messages m " \
                      f"INNER JOIN users u " \
                      f"ON m.user_id = u.id " \
                      f"WHERE m.time > :after"
    query_data = executeReadQuery(connection, select_messages, 1, {'after': after})

    for item in query_data:
        message = {'username': item[2], 'text': item[0], 'time': item[1]}
        new_messages.append(message)

    connection.close()
    return {"messages": new_messages}


@app.route("/send", methods=['POST'])
def send():
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

    if query_data is None:
        connection.close()
        return {'exist': False, 'match': False}

    password_hash = codec(query_data[0], 0)

    if not checkPassword(password.encode(), password_hash):
        connection.close()
        return {'exist': True, 'match': False}

    is_online = f"UPDATE users " \
                f"SET is_active = 1 " \
                f"WHERE username LIKE :username"
    executeQuery(connection, is_online, {'username': username})

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
        create_user = f"INSERT INTO users (username, password_hash, registered)" \
                      f"VALUES (:username, :password_hash, strftime('%s','now'))"
        executeQuery(connection, create_user, data_dict)
    else:
        connection.close()
        return {"loginOutOfRange": False, "passwordOutOfRange": False, 'ok': False}

    connection.close()
    return {"loginOutOfRange": False, "passwordOutOfRange": False, 'ok': True}


@app.route("/command", methods=['POST'])
def runCommand():
    """
    Execute command

    request: {
        "command": str
    }
    response: {
        "ok": bool,
        "output": str
    }
    """
    username = request.json["username"]
    cmd_with_args = request.json["command"]
    cmd_with_args = cmd_with_args.split()

    command = cmd_with_args[0]
    args = cmd_with_args[1:] if len(cmd_with_args) > 1 else None

    if command in [cmd['name'] for cmd in user_server_commands]:
        func = globals()[command]

        if args:
            output = func(username, args)
        else:
            output = func(username)

        return {'ok': True, 'output': output}
    else:
        return {'ok': False, 'output': 'An error occured'}


@app.route("/logout", methods=['POST'])
def logoutUser():
    """
    Mark that user loged out

    request: {
        "username": str
    }
    response: {
        "ok": bool
    }
    """
    username = request.json["username"]

    if username:
        connection = createConnection("data.sqlite3")
        logout_user = f"UPDATE users " \
                      f"SET is_active = 0, last_active = strftime('%s','now')" \
                      f"WHERE username LIKE :username"
        executeQuery(connection, logout_user, {'username': username})
        connection.close()

    return {"ok": True}


app.run()
