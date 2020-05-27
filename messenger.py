from datetime import datetime
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import clientui
from clicklabel import clickable


def close(window):
    window.close()


class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        self.sendButton.pressed.connect(self.send)
        self.signUpButton.pressed.connect(self.signUpUser)
        self.loginButton.pressed.connect(self.loginUser)
        self.textEdit.installEventFilter(self)
        self.last_message_time = 0
        self.username = None
        self.password = None
        self.warningMessages = {
            "emptyStr": '<html><head/><body><p><br/></p></body></html>',
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
        }
        self.user_client_commands = [
            {'name': 'close', 'description': 'Close the messenger'},
            {'name': 'logout', 'description': 'Logout from account'},
        ]
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)
        clickable(self.signUpLabel).connect(self.goToRegistration)
        clickable(self.loginLabel).connect(self.goToLogin)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
            if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus():
                self.send()
                return True
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            try:
                requests.post(
                    'http://127.0.0.1:5000/exit',
                    json={"username": self.username}, verify=False
                )
            except requests.exceptions.RequestException as e:
                print(e)
                raise SystemExit
            event.accept()
        else:
            event.ignore()

    def goToRegistration(self):
        self.stackedWidget.setCurrentIndex(1)

    def goToLogin(self):
        self.stackedWidget.setCurrentIndex(0)

    def signUpUser(self):
        self.loginError2.setText(self._translate("Messenger", self.warningMessages['emptyStr']))
        self.passwordError2.setText(self._translate("Messenger", self.warningMessages['emptyStr']))
        self.loginLine2.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine2.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine2.text()
        self.password = self.passwordLine2.text()

        if not self.username:
            if not self.password:
                self.loginError2.setText(self._translate("Messenger", self.warningMessages['loginRequired']))
                self.passwordError2.setText(self._translate("Messenger", self.warningMessages['passwordRequired']))
                self.loginLine2.setStyleSheet("border: 1px solid red")
                self.passwordLine2.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError2.setText(self._translate("Messenger", self.warningMessages['loginRequired']))
                self.loginLine2.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError2.setText(self._translate("Messenger", self.warningMessages['passwordRequired']))
                self.passwordLine2.setStyleSheet("border: 1px solid red")
                return

        if not self.username.isalnum():
            self.loginError2.setText(self._translate("Messenger", self.warningMessages['notAlphanumeric']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/signup',
                auth=(self.username, self.password),
                verify=False
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit

        if response.json()['loginOutOfRange']:
            self.loginError2.setText(self._translate("Messenger", self.warningMessages['loginOutOfRange']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return
        elif response.json()['passwordOutOfRange']:
            self.passwordError2.setText(self._translate("Messenger", self.warningMessages['passwordOutOfRange']))
            self.passwordError2.adjustSize()
            self.passwordLine2.setStyleSheet("border: 1px solid red")
            return
        elif not response.json()['ok']:
            self.loginError2.setText(self._translate("Messenger", self.warningMessages['registered']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return

        self.stackedWidget.setCurrentIndex(2)

    def loginUser(self):
        self.loginError1.setText(self._translate("Messenger", self.warningMessages['emptyStr']))
        self.passwordError1.setText(self._translate("Messenger", self.warningMessages['emptyStr']))
        self.loginLine1.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine1.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine1.text()
        self.password = self.passwordLine1.text()

        if not self.username:
            if not self.password:
                self.loginError1.setText(self._translate("Messenger", self.warningMessages['loginRequired']))
                self.passwordError1.setText(self._translate("Messenger", self.warningMessages['passwordRequired']))
                self.loginLine1.setStyleSheet("border: 1px solid red")
                self.passwordLine1.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError1.setText(self._translate("Messenger", self.warningMessages['loginRequired']))
                self.loginLine1.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError1.setText(self._translate("Messenger", self.warningMessages['passwordRequired']))
                self.passwordLine1.setStyleSheet("border: 1px solid red")
                return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/auth',
                auth=(self.username, self.password),
                verify=False
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit

        if not response.json()['exist']:
            self.loginError1.setText(self._translate("Messenger", self.warningMessages['invalidLogin']))
            self.loginLine1.setStyleSheet("border: 1px solid red")
            return
        if not response.json()['match']:
            self.passwordError1.setText(self._translate("Messenger", self.warningMessages['invalidPassword']))
            self.passwordLine1.setStyleSheet("border: 1px solid red")
            return

        self.stackedWidget.setCurrentIndex(2)

    def send(self):
        text = self.textEdit.toPlainText()
        text = text.strip()

        if not text:
            return
        elif text.startswith('/'):
            self.sendCommand(text[1:])
        else:
            self.sendMessage(text)

    def sendMessage(self, text):
        try:
            requests.post(
                'http://127.0.0.1:5000/send',
                json={"username": self.username, "text": text},
                verify=False
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit

        self.textEdit.clear()
        self.textEdit.repaint()

    def sendCommand(self, cmd_string):
        command = cmd_string.split()[0]
        args = cmd_string.split()[1:] if len(cmd_string) > 1 else None

        if command in [cmd['name'] for cmd in self.user_client_commands]:
            func = globals()[command]
            func(self)
            self.textEdit.clear()
            return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/command',
                json={"username": self.username, "command": 'help'}, verify=False
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit

        if not response.json()['ok']:
            self.addText(response.json()['output'] + "\n")
            self.textEdit.clear()
            return

        server_commands = response.json()['output']
        if command not in [cmd['name'] for cmd in server_commands]:
            self.addText(f"Command '{command}' not found.")
            self.addText("Try '/help' to list all available commands :)\n")
            self.textEdit.clear()
            return

        elif command == 'help':
            for cmd in self.user_client_commands:
                self.addText('{name:<10} - {description:<}'.format(**cmd))

            for cmd in server_commands:
                self.addText('{name:<10} - {description:<}'.format(**cmd))

            self.addText('')
            self.textEdit.clear()
            return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/command',
                json={"username": self.username, "command": cmd_string}, verify=False
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit

        if not response.json()['ok']:
            self.addText(response.json()['output'] + "\n")
            self.textEdit.clear()
            return

        if command == 'online':
            users = response.json()['output']
            reg_usernames = [user[0] for user in users]
            users_info = ''

            if args:

                if len(args) > len(users):
                    unregistered = [user for user in args if user not in reg_usernames]
                    not_exist = ', '.join(unregistered)
                    if len(unregistered) > 1:
                        self.addText("They aren't registered:")
                        self.addText(not_exist)
                        self.addText("You can type '/registered' to see registered users\n")
                    else:
                        self.addText(f"{not_exist} isn't registered\n")

                for user in users:
                    if user[1] == 1:
                        users_info += f"{user[0]} is online\n"
                    else:
                        beauty_time = datetime.fromtimestamp(user[2])
                        beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
                        users_info += f"{user[0]} was online at {beauty_time}\n"

                if users_info:
                    self.addText(users_info)

            else:
                online_count = len(reg_usernames)

                if online_count > 1:
                    users_info = ', '.join(reg_usernames)
                    self.addText(f"There are currently {online_count} users online:")
                    self.addText(users_info + "\n")
                else:
                    self.addText("Nobody is online now apart of you\n")

        elif command == 'status':
            status = response.json()['output']
            self.addText("######Server Status######")
            self.addText(f"Server date&time: {status['time']}")
            self.addText(f"Registered users: {status['users_count']}")
            self.addText(f"Written messages: {status['messages_count']}\n")

        elif command == 'myself':
            myself = response.json()['output']
            myself[2] = datetime.fromtimestamp(myself[2]).strftime('%Y/%m/%d %H:%M:%S')
            myself[3] = datetime.fromtimestamp(myself[3]).strftime('%Y/%m/%d %H:%M:%S')
            self.addText("######Your information######")
            self.addText(f"Your id: {myself[0]}")
            # 3 - admin, 2 - moderator, 1 - user
            self.addText(f"Permissions: {'administrator' if myself[1]==3 else 'user'}")
            self.addText(f"Registration date&time: {myself[2]}")
            self.addText(f"Previous activity: {myself[3]}\n")

        elif command == 'registered':
            all_usernames = response.json()['output']
            all_usernames = sum(all_usernames, [])
            all_usernames = ', '.join([username for username in all_usernames])
            self.addText(f"Registered users: {all_usernames}\n")

        self.textEdit.clear()
        self.textEdit.repaint()

    def getUpdates(self):
        if not self.stackedWidget.currentIndex() == 2:
            return

        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.last_message_time},
                verify=False
            )
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit

        for message in data['messages']:
            # float -> datetime
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
            self.addText(message['username'] + ' ' + beauty_time)
            self.addText(message['text'] + "\n")
            self.last_message_time = message['time']

    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()


app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()
app.exec_()
