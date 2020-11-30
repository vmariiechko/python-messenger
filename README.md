# Python Messenger

[![python]][pypi-url]
[![flask]][flask-url]
[![sqlite]][sqlite-url]
[![pyqt]][pyqt-url]
[![windows]][windows-url]
[![linux]][linux-url]
[![license]][license-url]

This is a python single-chat application separated on client-side and server-side.
General-purpose of the project is to message between hosts in the local network.
Additionally, you can [download](#download) a desktop application in two versions.

![demo-login] ![demo-preferences]
![demo-shortcuts] &nbsp;&nbsp; ![demo-chat]

---

## Table of content

- [Installation](#installation)
- [Usage](#usage)
- [Download](#download)
- [Features](#features)
- [License](#license)

---

## Installation

Clone the project from GitHub, then you'll need [Git](https://git-scm.com/) 
installed on your computer:

```
# Clone this repository
$ git clone https://github.com/marik348/python-messegner
```

---

## Usage

The next steps explain how to use the messenger in your local network.

To run this application, you'll need [Python 3.6+](https://www.python.org/) 
installed on your computer.
In your [working environment][venv-url] from the command line:

```
# Go into the repository
$ cd python-messenger

# Install dependencies
$ pip3 install -r requirements.txt
```

Once you've installed all the dependencies, run the server on your local 
network in the first command prompt with arguments [username] [password] 
to create an administrator account:

```
# Navigate to server-side
$ cd ./messenger/server

# Run server and create [username] with administrator role 
$ python server.py [username] [password]
```

From that moment, your computer will work as a server (receive requests)
in the local network.
You can stop the server with Ctrl+C combination pressed twice in the terminal.
Next time it's not necessary to run the server with arguments to create an 
admin account unless you've deleted the ```database.sqlite3``` file.

After running the server, everyone from your network can run a messenger.
Go to the root directory of the project and 
run the messenger client in the second command line prompt:

```
# Navigate to client-side
$ cd ./messenger/client

# Run client
$ python messenger.py
```

To connect to the server, everyone from your local network should
change the IP address in Preferences to [the local IP address](https://www.whatismybrowser.com/detect/what-is-my-local-ip-address) 
with 9000 port (the local IP of the computer which runs the server).

Register an account or log in to the administrator account.
Finally, you can use the messenger to communicate in the local network. 

P.S. Originally project was developed on Debian family distribution, 
that's why it causes some UI problems on Windows.

---

## Download

There are two executable desktop versions with the ability to chat in the:

1. local network
2. global network

Get them for Windows and Linux from [here](https://github.com/marik348/python-messegner/releases/tag/v1.2.0).

The main difference between versions is that the second one
has the deployed server IP address by default
without the ability to change the IP address in Preferences.

---

## Features

* Shortcuts
* Gradient Design
* Lots of commands
* Ability to change a server IP address
* Ability to check server status in the login form
* Ability to promote/demote users (for admins)
* Ability to ban users (for moderators and above)
* Cross-platform
  - Windows and Linux ready

### There are 3 roles in messenger:

- **User:** Has standard commands
- **Moderator:** The above + permissions to ban/unban users
- **Administrator:** All the above + the ability to change the role of the user

### Available user commands:

COMMAND | VARIABLES | DESCRIPTION
--------|-----------|--------------------------
/close  |           | Closes the messenger
/logout |           | Logs out from the account
/reload |           | Clears commands messages
/help   | [command] | Prints available commands or detailed description about [command] if specified
/myself |           | Prints info about user
/status |           | Prints server status
/online | [users]   | Prints online users or [users] status if specified
/reg    |           | Prints registered users

### Available moderator commands:

COMMAND | VARIABLES  | DESCRIPTION
--------|------------|--------------
/ban    | [users]    | Bans [users]
/unban  | [users]    | Unbans [users]

### Available administrator commands:

COMMAND | VARIABLES    | DESCRIPTION
--------|--------------|--------------------
/role   | [user] [1-3] | Changes [user] role

---

## License

>You can check out the full license [here][license-url].

This project is licensed under the terms of the **MIT** license.

---

> Gmail [vadimich348@gmail.com](mailto:vadimich348@gmail.com) &nbsp;&middot;&nbsp;
> GitHub [@marik348](https://github.com/marik348) &nbsp;&middot;&nbsp;
> LinkedIn [@mariiechko](https://www.linkedin.com/in/mariiechko/)

<!-- Markdown links and images -->
[python]: https://img.shields.io/badge/Python%203.6+-14354C?style=for-the-badge&logo=python&logoColor=white
[flask]: https://img.shields.io/badge/flask-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white
[pyqt]: https://img.shields.io/badge/pyqt5-%2341CD52.svg?&style=for-the-badge&logo=qt&logoColor=white
[windows]: https://img.shields.io/badge/windows-0078D6?logo=windows&logoColor=white&style=for-the-badge
[linux]: https://img.shields.io/badge/linux-%23d6d6d6?logo=linux&logoColor=black&style=for-the-badge
[license]: https://img.shields.io/badge/license-MIT-%2341CD52.svg?&style=for-the-badge

[pypi-url]: https://pypi.org/project/py-messenger/
[flask-url]: https://pypi.org/project/Flask/
[sqlite-url]: https://docs.python.org/3/library/sqlite3.html
[pyqt-url]: https://pypi.org/project/PyQt5/#description
[windows-url]: https://www.microsoft.com/en-us/windows/
[linux-url]: https://linuxmint.com/
[license-url]: https://github.com/marik348/python-messegner/blob/master/LICENSE.txt

[demo-login]: https://i.imgur.com/TmN0v1t.png
[demo-preferences]: https://i.imgur.com/znQcrxJ.png
[demo-shortcuts]: https://i.imgur.com/xROErgP.png
[demo-chat]: https://i.imgur.com/fYqpBCe.png

[venv-url]: https://docs.python.org/3/tutorial/venv.html
