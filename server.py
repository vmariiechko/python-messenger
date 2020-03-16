import time
import sqlite3
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)
messages = [
    {'username': 'Jack', 'text': 'Hello', 'time': time.time()},
    {'username': 'Mary', 'text': 'Hi, jack!', 'time': time.time()}
]
users = {
    # username: password
    'Jack': '12345',
    'Mary': '54321',
    'Admin': 'admin'
}

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                username text, password text
                )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
                username text, password text, message text, time integer
                )""")
conn.close()


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
    return {
        "status": True,
        "time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "users_count": len(users),
        "messages_count": len(messages),
    }


@app.route("/messages")
def messagesView():
    """
    Receive messages after point "after"

    request: ?after=1234567890.4567
    response: {
        "messages": [
            {"username": "str", "text": "str", "time": float},
            ...
        ]
    }
    """
    after = float(request.args['after'])
    new_messages = [message for message in messages if message["time"] > after]
    return {"messages": new_messages}


@app.route("/send", methods=['POST'])
def sendView():
    """
    Send message

    request: {
        "username": str,
        "password": str,
        "text": str
    }
    response: {"ok": bool}
    """
    date = request.json
    username = date["username"]
    text = date["text"]

    new_message = {"username": username, "text": text, "time": time.time()}
    messages.append(new_message)

    return {'ok': True}


@app.route("/auth", methods=['POST'])
def authUser():
    date = request.json
    username = date["username"]
    password = date["password"]

    if username not in users:
        return {'exist': False, 'match': False}

    if users[username] != password:
        return {'exist': True, 'match': False}

    return {'exist': True, 'match': True}


@app.route("/signup", methods=['POST'])
def signupUser():
    date = request.json
    username = date["username"]
    password = date["password"]

    if len(username) not in range(4, 20, 1):
        return {"loginOutOfRange": True}
    elif len(password) not in range(4, 20, 1):
        return {"loginOutOfRange": False, "passwordOutOfRange": True}

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=:username", {'username': username})
    data = cursor.fetchone()

    if data is None:
        cursor.execute("INSERT INTO users VALUES (:username, :password)", {'username': username, 'password': password})
        users[username] = password
    else:
        return {"loginOutOfRange": False, "passwordOutOfRange": False, 'ok': False}

    conn.commit()
    conn.close()
    return {"loginOutOfRange": False, "passwordOutOfRange": False, 'ok': True}


app.run()
