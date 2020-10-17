def getWarningMessages():
    return {"emptyStr": '<html><head/><body><p><br/></p></body></html>',
            "registered": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Username '
                          'is already registered</span></p></body></html> ',
            "loginRequired": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Login is '
                             'required</span></p></body></html>',
            "invalidLogin": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Username '
                            'doesn\'t exist</span></p></body></html> ',
            "loginOutOfRange": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Username '
                               'must be between 4 and 20 in length</span></p></body></html> ',
            "passwordRequired": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Password is '
                                'required</span></p></body></html> ',
            "invalidPassword": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Password '
                               'doesn\'t match</span></p></body></html> ',
            "passwordOutOfRange": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Password '
                                  'must be between 4 and 20 in length</span></p></body></html> ',
            "notAlphanumeric": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Login can '
                               'only contain alphanumeric characters</span></p></body></html>',
            "banned": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Account '
                      'was banned</span></p></body></html>',
            }


def getClientCommands():
    return [
            {'name': 'close', 'description': 'Close the messenger',
             'detailed': '<b>Usage:</b> /close<br>'
                         'Ask you to close messenger.'},
            {'name': 'logout', 'description': 'Logout account',
             'detailed': '<b>Usage:</b> /logout<br>'
                         'Ask you to logout account.'},
            {'name': 'reload', 'description': 'Clear commands messages',
             'detailed': '<b>Usage:</b> /reload<br>'
                         'Clear all commands` messages.'},
            ]


def getMessageBoxText():
    return {"close": "<span style=\"font-size: 15px\">Are you sure to quit?</span>",
            "logout": "<span style=\"font-size: 15px\">Are you sure to logout?</span>",
            "about": "<span style=\"font-size: 15px\">"
                         "Messenger **.**.2020<br>"
                         "Version: 1.1"
                     "</span><br><br>"
                         "Created by Vadym Mariiechko",
            "contacts": "<span style=\"font-size: 15px\">"
                            "Vadym Mariiechko:<br>"
                            "LinkedIn: <a href='http<h5>s://www.linkedin.com/in/mariiechko/'>mariiechko</a><br>"
                            "GitHub: <a href='https://github.com/marik348'>marik348</a>"
                        "</span> ",
            "serverIsOff": "<span style=\"font-size: 15px\">The server is offline</span>",
            "shortcuts": "<span style=\"font-size: 14px\"><table>"
                            "<tr>"
                                "<th>Shortcuts&nbsp;&nbsp;</th>"
                                "<th>Description</th>"
                            "</tr>"
                            "<tr>"
                                "<td><code>Cntrl+A</code></td>"
                                "<td>Account settings</td>"
                            "</tr>"
                            "<tr>"
                                "<td><code>Cntrl+R</code></td>"
                                "<td>Open preferences</td>"
                            "</tr>"
                            "<tr>"
                                "<td><code>Cntrl+S</code></td>"
                                "<td>Show available shortcuts</td>"
                            "</tr>"
                            "<tr>"
                                "<td><code>Cntrl+D</code></td>"
                                "<td>Show available commands</td>"
                            "</tr>"
                            "<tr>"
                                "<td><code>Enter</code></td>"
                                "<td>Send message</td>"
                            "</tr>"
                        "</table></span>"
            }
