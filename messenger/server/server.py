from datetime import datetime
from sqlite3 import Binary
from sys import argv

from flask import Flask, request

import messages_overflow
from server_commands import (user_server_commands, moderator_server_commands, admin_server_commands,
                             help_client, myself, get_online, get_registered, ban, unban, change_role)
from database import (create_connection, execute_query, execute_read_query)
from codec import (codec, generate_key, hash_password, check_password)

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
                                );"""
}

available_commands = {'help': help_client,
                      'myself': myself,
                      'online': get_online,
                      'reg': get_registered,
                      'ban': ban,
                      'unban': unban,
                      'role': change_role}

# Create database, if not created
connection = create_connection("data.sqlite3")
execute_query(connection, queries['create_users_table'])
execute_query(connection, queries['create_messages_table'])

# Create administrator, if the server was run with arguments [username] [password]
if len(argv) == 3:
    password_hash = codec(argv[2], 1)
    password_hash = Binary(password_hash)

    data_dict = {'username': argv[1], 'password_hash': password_hash}
    create_admin = f"INSERT INTO users (username, password_hash, role, registered)" \
                   f"VALUES (:username, :password_hash, 3, strftime('%s','now'))"
    execute_query(connection, create_admin, data_dict)
else:
    print("ATTENTION: You haven't specified 2 additional arguments: [username] [password]\n"
          "An account with administrator role wasn't created\n")

connection.close()


@app.route("/")
def hello():
    """Prints hello message in root route."""

    return "<h1>My First Python Program</h1>"


@app.route("/status")
def status(*args):
    """
    Calculates server time, amount of users, online users & messages.

    :return: dict of all calculated data
    :rtype: {
        "status": bool,
        "time": str,
        "users_count": int,
        "messages_count": int,
        "users_online": int
    }
    """

    connection = create_connection("data.sqlite3")

    select_users_count = "SELECT Count(*) FROM users"
    users_count = execute_read_query(connection, select_users_count, 0)

    select_messages_count = "SELECT Count(*) FROM messages"
    messages_count = execute_read_query(connection, select_messages_count, 0)

    users_online = len(get_online(None, None))

    connection.close()
    return {
        "status": True,
        "time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "users_count": users_count[0],
        "messages_count": messages_count[0],
        "users_online": users_online,
    }


@app.route("/get_messages")
def get_messages():
    """
    Collects new messages after specified point of time.

    :request: ?after=1234567890.4 - point of time
    :return: new messages after specified point
    :rtype: {
        "messages": [
            {"username": str, "text": str, "time": float},
            ...
        ]
    }
    """

    after_time = float(request.args['after'])
    new_messages = []

    connection = create_connection("data.sqlite3")

    select_messages = f"SELECT m.text, m.time, u.username FROM messages m " \
                      f"INNER JOIN users u " \
                      f"ON m.user_id = u.id " \
                      f"WHERE m.time > :after"
    query_data = execute_read_query(connection, select_messages, 1, {'after': after_time})

    # Generate messages.
    for data in query_data:
        message = {'username': data[2], 'text': data[0], 'time': data[1]}
        new_messages.append(message)

    connection.close()
    return {"messages": new_messages}


@app.route("/send_message", methods=['POST'])
def send_message():
    """
    Stores the message, time of sending and username of author in database.

    :request: {
        "username": str,
        "text": str
    }
    :return: dict of execution status
    :rtype: {"ok": bool}
    """

    data = request.json
    username = data["username"]
    text = data["text"]

    connection = create_connection("data.sqlite3")

    select_user_id = f"SELECT id FROM users WHERE username LIKE :username"
    query_data = execute_read_query(connection, select_user_id, 0, {'username': username})

    data_dict = {'text': text, 'id': query_data[0]}
    new_message = f"INSERT INTO messages (text, time, user_id) " \
                  f"VALUES (:text, strftime('%s','now'), :id)"
    execute_query(connection, new_message, data_dict)

    connection.close()
    return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_user():
    """
    Verifies user exists, password matches and whether user is banned.

    request: {
        "username": str,
        "password": str
    }
    :return: dict of execution status
    :rtype: {
        "exist": bool,
        "match": bool,
        "banned": bool
    }
    """

    username = request.authorization.username
    password = request.authorization.password

    connection = create_connection("data.sqlite3")

    select_user = f"SELECT password_hash, is_banned  FROM users WHERE username LIKE :username"
    query_data = execute_read_query(connection, select_user, 0, {'username': username})

    if query_data is None:
        connection.close()
        return {'exist': False}

    # Decrypt password hash.
    password_hash = codec(query_data[0], 0)

    # Compare entered password and hash from database.
    if not check_password(password.encode(), password_hash):
        connection.close()
        return {'exist': True, 'match': False}

    # Check if user is banned.
    elif query_data[1] == 1:
        connection.close()
        return {'exist': True, 'match': True, 'banned': True}

    set_online = f"UPDATE users " \
                 f"SET is_active = 1 " \
                 f"WHERE username LIKE :username"
    execute_query(connection, set_online, {'username': username})

    connection.close()
    return {'exist': True, 'match': True, 'banned': False}


@app.route("/sign_up", methods=['POST'])
def sign_up_user():
    """
    Register user.

    Confirms whether login and password are in range and whether user exist.
    Hashes and encrypts password using :func:`codec`.
    Stores user's data in database.

    request: {
        "username": str,
        "password": str
    }
    :return: dict of execution status
    :rtype: {
        "login_out_of_range": bool,
        "password_out_of_range": bool,
        "ok": bool
    }
    """

    username = request.authorization.username
    password = request.authorization.password

    # Make sure credentials are in range.
    if len(username) not in range(4, 20, 1):
        return {"login_out_of_range": True}
    elif len(password) not in range(4, 20, 1):
        return {"login_out_of_range": False, "password_out_of_range": True}

    connection = create_connection("data.sqlite3")

    select_user = f"SELECT id FROM users WHERE username LIKE :username"
    query_data = execute_read_query(connection, select_user, 0, {'username': username})

    # If user isn't registered, encrypt password and store in database.
    if query_data is None:
        password_hash = codec(password, 1)
        password_hash = Binary(password_hash)

        data_dict = {'username': username, 'password_hash': password_hash}
        create_user = f"INSERT INTO users (username, password_hash, registered)" \
                      f"VALUES (:username, :password_hash, strftime('%s','now'))"
        execute_query(connection, create_user, data_dict)

    else:
        connection.close()
        return {"login_out_of_range": False, "password_out_of_range": False, 'ok': False}

    connection.close()
    return {"login_out_of_range": False, "password_out_of_range": False, 'ok': True}


@app.route("/command", methods=['POST'])
def execute_command():
    """
    Executes command.

    request: {
        "username": str,
        "command": str
    }
    :return: dict of execution status and output of command
    :rtype: {
        "ok": bool,
        "output": str
    }
    """

    username = request.json["username"]
    cmd_with_args = request.json["command"]

    cmd_with_args = cmd_with_args.split()

    # Separate command from arguments.
    command_name = cmd_with_args[0]
    args = cmd_with_args[1:] if len(cmd_with_args) > 1 else None

    # Execute command with user permissions.
    if command_name in [cmd['name'] for cmd in user_server_commands]:
        command_func = available_commands.get(command_name)

        if args:
            output = command_func(username, args)
        else:
            output = command_func(username)

        return {'ok': True, 'output': output}

    # Execute command with moderator/admin permissions.
    elif command_name in [cmd['name'] for cmd in moderator_server_commands + admin_server_commands]:
        if not args:
            return {'ok': False, 'output': 'Argument must be specified'}

        command_func = available_commands.get(command_name)

        output = command_func(username, args)

        return {'ok': output['ok'], 'output': output['result']}

    else:
        return {'ok': False, 'output': 'An error occured'}


@app.route("/logout", methods=['POST'])
def logout_user():
    """
    Marks that user logged out.

    request: {
        "username": str
    }
    :return: dict of execution status
    :rtype: {"ok": bool}
    """

    username = request.json["username"]

    if username:
        connection = create_connection("data.sqlite3")

        logout_user = f"UPDATE users " \
                      f"SET is_active = 0, last_active = strftime('%s','now')" \
                      f"WHERE username LIKE :username"
        execute_query(connection, logout_user, {'username': username})

        connection.close()

    return {"ok": True}


available_commands['status'] = status
app.run(host="0.0.0.0", port=9000)
