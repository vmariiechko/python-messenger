import sqlite3
import threading
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
    {'name': 'help', 'description': 'Prints available commands',
     'detailed': '#Usage: /help <command>\n\n'
                 'Prints available commands if no argument.\n'
                 'Prints detailed description of <command> If argument <command> is specified.\n\n'
                 '#Examples:\n'
                 '/help  ->  prints all available commands\n'
                 '/help reg  ->  prints detailed info about \'/reg\''},
    {'name': 'myself', 'description': 'Prints info about you',
     'detailed': '#Usage: /myself\n'
                 'Prints next information about you:\n'
                 'ID, role, registration date, last activity.'},
    {'name': 'status', 'description': 'Prints server status',
     'detailed': '#Usage: /status\n'
                 'Prints next information about server:\n'
                 'Server time, registered users count, written messages count.'},
    {'name': 'online', 'description': 'Prints online users',
     'detailed': '#Usage: /online <usernames>\n\n'
                 'Prints online users if there are no argument.\n'
                 'If <usernames> specified, prints users status.\n\n'
                 '#Examples:\n'
                 '/online  ->  prints all online users\n'
                 '/online User1 User2  ->  prints User1 & User2 status'},
    {'name': 'reg', 'description': 'Prints registered users',
     'detailed': '#Usage: /reg\n'
                 'Prints usernames of all registered users.'},
]
moderator_server_commands = [
    {'name': 'ban', 'description': 'Ban users',
     'detailed': '#Usage: /ban <usernames>\n\n'
                 'Ban specified <usernames>\n\n'
                 '#Example:\n'
                 '/ban User1 User2 -> ban User1 and User2'},
    {'name': 'unban', 'description': 'Unban users',
     'detailed': '#Usage: /unban <usernames>\n\n'
                 'Unban specified <usernames>\n\n'
                 '#Example:\n'
                 '/unban User1 User2 -> unban User1 and User2,'},
]
admin_server_commands = [
    {'name': 'role', 'description': 'Change role of user',
     'detailed': "#Usage: /role <username> <role>\n\n"
                 "Change user permissions.\n"
                 "Argument <role> can be '1', '2' or '3'\n"
                 "Where 1-user, 2-moderator, 3-administrator\n\n"
                 "#Example:\n"
                 "/role Bob 2  ->  change Bob's role to 'moderator'"},
]

connection = createConnection("data.sqlite3")
executeQuery(connection, queries['create_users_table'])
executeQuery(connection, queries['create_messages_table'])
connection.close()


def checkPermissions(username):
    connection = createConnection("data.sqlite3")

    select_permission = f"SELECT role " \
                        f"FROM users " \
                        f"WHERE username LIKE :username"

    query_data = executeReadQuery(connection, select_permission, 0, {'username': username})

    connection.close()
    return query_data


def help(username, args=None):
    role = checkPermissions(username)

    if role[0] == 3:
        return user_server_commands + moderator_server_commands + admin_server_commands
    elif role[0] == 2:
        return user_server_commands + moderator_server_commands
    else:
        return user_server_commands


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

    select_user = f"SELECT id, role, registered, last_active " \
                  f"FROM users " \
                  f"WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_user, 0, {'username': username})

    connection.close()
    return query_data


def reg(username, args=None):
    connection = createConnection("data.sqlite3")

    all_usernames = queries['select_all_usernames']
    query_data = executeReadQuery(connection, all_usernames)

    connection.close()
    return query_data


def role(username, args):
    permission = args[-1]  # TODO move all parse steps to client after moving commands to file
    if permission not in ('1', '2', '3'):
        return {'ok': False, 'result': "Role isn't specified"}
    elif len(args) != 2:
        return {'ok': False, 'result': "Enter username"}

    all_usernames = reg(username)
    user = args[0]

    if user not in [usernames[0] for usernames in all_usernames]:
        return {'ok': False, 'result': "User doesn't exist"}

    if user == username:
        return {'ok': False, 'result': "It's not allowed to change permissions for yourself"}

    connection = createConnection("data.sqlite3")
    data_dict = {'permission': permission, 'username': user}

    update_role = f"UPDATE users " \
                  f"SET role = :permission " \
                  f"WHERE username LIKE :username"
    executeQuery(connection, update_role, data_dict)

    connection.close()
    return {'ok': True, 'result': '\'s permissions was updated successfully\n'}


def ban(username, args, flag=1):
    all_usernames = reg(username)
    all_usernames = sum(all_usernames, ())

    if not all(username in all_usernames for username in args):
        return {'ok': False, 'result': 'Not all users exist'}

    connection = createConnection("data.sqlite3")

    if flag:
        ban_users = f"UPDATE users " \
                    f"SET is_banned = 1 " \
                    f"WHERE username IN ({','.join(['?'] * len(args))})" \
                    f"AND role = 1"
        executeQuery(connection, ban_users, args)
        result = 'Only users were banned\n'
    else:
        unban_users = f"UPDATE users " \
                      f"SET is_banned = 0 " \
                      f"WHERE username IN ({','.join(['?'] * len(args))})"
        executeQuery(connection, unban_users, args)
        result = 'Users were unbanned\n'

    connection.close()
    return {'ok': True, 'result': result}


def unban(username, args):
    return ban(username, args, 0)


@app.route("/")
def hello():
    return "<h1>My First Python Messenger</h1>"


@app.route("/status")
def status(username=None, args=None):  # TODO change arguments / reimplement module after moving commands to file
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

    select_user = f"SELECT password_hash, is_banned  FROM users WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_user, 0, {'username': username})

    if query_data is None:
        connection.close()
        return {'exist': False}

    password_hash = codec(query_data[0], 0)

    if not checkPassword(password.encode(), password_hash):
        connection.close()
        return {'exist': True, 'match': False}

    elif query_data[1] == 1:
        return {'exist': True, 'match': True, 'banned': True}

    is_online = f"UPDATE users " \
                f"SET is_active = 1 " \
                f"WHERE username LIKE :username"
    executeQuery(connection, is_online, {'username': username})

    connection.close()
    return {'exist': True, 'match': True, 'banned': False}


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

    select_user = f"SELECT id FROM users WHERE username LIKE :username"
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
        "username": str
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
    permissions = checkPermissions(username)

    print("Server Role: ")
    print(permissions[0])

    command = cmd_with_args[0]
    args = cmd_with_args[1:] if len(cmd_with_args) > 1 else None

    if command in [cmd['name'] for cmd in user_server_commands]:
        func = globals()[command]

        if args:
            output = func(username, args)
        else:
            output = func(username)

        return {'ok': True, 'output': output}

    elif command in [cmd['name'] for cmd in moderator_server_commands]:
        if permissions[0] < 2:
            return {'ok': False, 'output': 'An error occured'}
        elif not args:
            return {'ok': False, 'output': 'Argument must be specified'}

        func = globals()[command]

        output = func(username, args)

        return {'ok': output['ok'], 'output': output['result']}

    elif command in [cmd['name'] for cmd in admin_server_commands]:
        if permissions[0] != 3:
            return {'ok': False, 'output': 'An error occured'}
        elif not args:
            return {'ok': False, 'output': 'Argument must be specified'}

        func = globals()[command]

        output = func(username, args)

        return {'ok': output['ok'], 'output': output['result']}

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
