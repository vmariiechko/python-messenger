def get_warning_messages():
    """Generates warning messages in HTML."""

    html_begin = '<span style=" font-style:italic; color:#ffffff;">'
    html_end = '</span>'

    warning_messages = {
        "empty_str": '',
        "registered": 'Username is already registered',
        "login_required": 'Login is required',
        "invalid_login": 'Username doesn\'t exist',
        "login_out_of_range": 'Username must be between 4 and 20 in length',
        "password_required": 'Password is required',
        "invalid_password": 'Password doesn\'t match',
        "password_out_of_range": 'Password must be between 4 and 20 in length',
        "not_alphanumeric": 'Login can only contain alphanumeric characters',
        "banned": 'Account was banned',
    }

    warning_messages = {key: html_begin + value + html_end for key, value in warning_messages.items()}

    return warning_messages


def get_client_commands():
    """Generates client-side commands."""

    return [
            {'name': 'close',
             'description': 'Close the messenger',
             'detailed': '<b>Usage:</b> /close<br><br>'
                         'Ask you to close messenger.'},
            {'name': 'logout',
             'description': 'Logout account',
             'detailed': '<b>Usage:</b> /logout<br><br>'
                         'Ask you to logout account.'},
            {'name': 'reload',
             'description': 'Clear commands messages',
             'detailed': '<b>Usage:</b> /reload<br><br>'
                         'Clear all commands` messages.'},
            ]


def get_message_box_text():
    """Generates text for message boxes in HTML."""

    html_begin = '<span style="font-size: 15px">'
    html_end = '</span>'

    shortcuts_table = "<table>" \
                            "<tr>" \
                                "<th>Shortcuts&nbsp;&nbsp;</th>" \
                                "<th>Description</th>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Ctrl+S</code></td>" \
                                "<td>Show available shortcuts</td>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Ctrl+D</code></td>" \
                                "<td>Show available commands</td>" \
                            "</tr>" \
                            "<tr>" \
                                "<td><code>Alt+G</code></td>" \
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
                        "about": "Messenger 12.2020<br>"
                                 "Version: 1.2"
                                 "<br><br>",
                        "contacts": "Vadym Mariiechko:<br><br>"
                                    "<a href='mailto:vadimich348@gmail.com'>vadimich348@gmail.com</a><br>"
                                    "LinkedIn: <a href='https://www.linkedin.com/in/mariiechko/'>mariiechko</a><br>"
                                    "GitHub: <a href='https://github.com/marik348'>marik348</a>",
                        "server_is_off": "The server is offline",
                        "shortcuts": shortcuts_table
                        }

    message_box_text = {key: html_begin + value + html_end for key, value in message_box_text.items()}
    message_box_text["about"] += "Created by Vadym Mariiechko"

    return message_box_text


def get_message_style():
    """Generates style for messages in HTML."""

    return {'begin': "<table style='text-align: right; margin-right: 5px;'><tr><td style='text-align: right;'>",
            'middle': "</td></tr><tr><td style='text-align: right;'>",
            'end': "</td></tr></table><br>",
            }
