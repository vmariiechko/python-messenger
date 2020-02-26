import time
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
    'Mary': '54321'
}


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
    password = date["password"]
    text = date["text"]

    if username in users:
        real_password = users[username]
        if real_password != password:
            return {"ok": False}
    else:
        users[username] = password

    new_message = {"username": username, "text": text, "time": time.time()}
    messages.append(new_message)

    return {'ok': True}


@app.route("/auth", methods=['POST'])
def authUser():
    date = request.json
    username = date["username"]
    password = date["password"]

    if username in users:
        real_password = users[username]
        if real_password != password:
            return {"ok": False}
    else:
        users[username] = password

    return {'ok': True}


app.run()
