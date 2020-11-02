def getWarningMessages():
    html_begin = '<span style=" font-style:italic; color:#ffffff;">'
    html_end = '</span>'

    warning_messages = {
        "emptyStr": '',
        "registered": 'Username is already registered',
        "loginRequired": 'Login is required',
        "invalidLogin": 'Username doesn\'t exist',
        "loginOutOfRange": 'Username must be between 4 and 20 in length',
        "passwordRequired": 'Password is required',
        "invalidPassword": 'Password doesn\'t match',
        "passwordOutOfRange": 'Password must be between 4 and 20 in length',
        "notAlphanumeric": 'Login can only contain alphanumeric characters',
        "banned": 'Account was banned',
    }

    warning_messages = {key: html_begin + value + html_end for key, value in warning_messages.items()}

    return warning_messages


def getClientCommands():
    return [
            {'name': 'close',
             'description': 'Close the messenger',
             'detailed': '<b>Usage:</b> /close<br>'
                         'Ask you to close messenger.'},
            {'name': 'logout',
             'description': 'Logout account',
             'detailed': '<b>Usage:</b> /logout<br>'
                         'Ask you to logout account.'},
            {'name': 'reload',
             'description': 'Clear commands messages',
             'detailed': '<b>Usage:</b> /reload<br>'
                         'Clear all commands` messages.'},
            ]


def getMessageBoxText():
    html_begin = '<span style="font-size: 15px">'
    html_end = '</span>'

    shortcuts_table = "<table>" \
                            "<tr>" \
                                "<th>Shortcuts&nbsp;&nbsp;</th>" \
                                "<th>Description</th>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Cntrl+S</code></td>" \
                                "<td>Show available shortcuts</td>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Cntrl+D</code></td>" \
                                "<td>Show available commands</td>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Cntrl+G</code></td>" \
                                "<td>Logout from accout</td>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Alt+E</code></td>" \
                                "<td>Close the messenger</td>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Enter</code></td>" \
                                "<td>Send message</td>" \
                            "</tr>" \
                        "</table>"

    message_box_text = {"close": "Are you sure to quit?",
                        "logout": "Are you sure to logout?",
                        "about": "Messenger **.**.2020<br>"
                                 "Version: 1.2"
                                 "<br><br>",
                        "contacts": "Vadym Mariiechko:<br><br>"
                                    "vadimich348@gmail.com<br>"
                                    "LinkedIn: <a href='http<h5>s://www.linkedin.com/in/mariiechko/'>mariiechko</a><br>"
                                    "GitHub: <a href='https://github.com/marik348'>marik348</a>",
                        "serverIsOff": "The server is offline",
                        "shortcuts": shortcuts_table
                        }

    message_box_text = {key: html_begin + value + html_end for key, value in message_box_text.items()}
    message_box_text["about"] += "Created by Vadym Mariiechko"

    return message_box_text


def getMessageStyle():
    return {'begin': "<table style='text-align: right; margin-right: 5px;'><tr><td style='text-align: right;'>",
            'middle': "</td></tr><tr><td style='text-align: right;'>",
            'end': "</td></tr></table><br>",
            }
