from requests import get, post, exceptions
from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont
from qtwidgets import PasswordEdit

from client_commands import *
from client_content import *
from click_label import clickable
from client_ui import Ui_Messenger
from preferences import PreferencesWindow

from style_sheet import load_stylesheet


class MessengerWindow(QtWidgets.QMainWindow, Ui_Messenger):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate

        self.passwordLine1 = PasswordEdit(True, self.Login_page)
        self.passwordLine2 = PasswordEdit(True, self.Registration_page)
        self.modifyPasswordLines()

        self.sendButton.pressed.connect(self.send)
        self.signUpButton.pressed.connect(self.signUpUser)
        self.loginButton.pressed.connect(self.loginUser)

        self.actionShortcuts.triggered.connect(self.showShortcutsBox)
        self.actionCommands.triggered.connect(self.showCommandsBox)
        self.actionAbout.triggered.connect(self.showAboutBox)
        self.actionContacts.triggered.connect(self.showContactsBox)
        self.actionPreferences.triggered.connect(self.openPreferencesWindow)
        self.actionLogout.triggered.connect(self.logout)
        self.actionClose.triggered.connect(self.close)

        self.plainTextEdit.installEventFilter(self)

        self.username = None
        self.password = None
        self.last_message_time = 0
        self.max_text_len = 250
        self.server_IP = '127.0.0.1:5000'

        self.warning_messages = getWarningMessages()
        self.message_box_text = getMessageBoxText()

        self.client_commands = getClientCommands()
        self.run_client_command = {'close': self.close,
                                   'logout': self.logout,
                                   'reload': self.reload}
        self.server_commands = []
        self.run_server_command = {}

        self.timerUpdates = QtCore.QTimer()
        self.timerUpdates.timeout.connect(self.getUpdates)
        self.timerUpdates.start(1000)

        self.timerStatus = QtCore.QTimer()
        self.timerStatus.timeout.connect(self.getStatus)
        self.timerStatus.start(5000)

        clickable(self.signUpLabel).connect(self.goToRegistration)
        clickable(self.loginLabel).connect(self.goToLogin)

        self.getStatus()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.plainTextEdit:
            text = self.plainTextEdit.toPlainText()

            if event.key() == QtCore.Qt.Key_Return and self.plainTextEdit.hasFocus():
                self.send()
                return True

            elif len(text) > self.max_text_len:
                text = text[:self.max_text_len]
                self.plainTextEdit.setPlainText(text)

                cursor = self.plainTextEdit.textCursor()
                cursor.setPosition(self.max_text_len)
                self.plainTextEdit.setTextCursor(cursor)
                return True

        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', self.message_box_text["close"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            try:
                post(
                    f'http://{self.server_IP}/logout',
                    json={"username": self.username}, verify=False
                )
            except exceptions.RequestException as e:
                print(e)
                raise SystemExit

            event.accept()
        else:
            event.ignore()

    def logout(self):
        reply = QMessageBox.question(self, 'Logout', self.message_box_text["logout"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            try:
                post(
                    f'http://{self.server_IP}/logout',
                    json={"username": self.username}, verify=False
                )
            except exceptions.RequestException as e:
                print(e)
                self.showServerOffBox()
                self.clearUserData()
                return

            self.goToLogin()
            self.clearUserData()
            self.actionLogout.setEnabled(False)
            self.actionCommands.setEnabled(False)
        else:
            return

    def modifyPasswordLines(self):
        geometry = QtCore.QRect(60, 200, 291, 41)
        font = QFont()
        font.setPointSize(14)

        self.passwordLine1.setGeometry(geometry)
        self.passwordLine1.setFont(font)
        self.passwordLine1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine1.setObjectName("passwordLine1")
        self.passwordLine1.setPlaceholderText(self._translate("Messenger", "Password"))

        self.passwordLine2.setGeometry(geometry)
        self.passwordLine2.setFont(font)
        self.passwordLine2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine2.setObjectName("passwordLine2")
        self.passwordLine2.setPlaceholderText(self._translate("Messenger", "Enter Your Password"))

    def openPreferencesWindow(self):
        dlg = PreferencesWindow(self)
        if dlg.exec():
            self.server_IP = dlg.serverIP.text()

    def clearUserData(self):
        self.username = None
        self.plainTextEdit.clear()
        self.textBrowser.clear()
        self.last_message_time = 0

    def reload(self):
        self.textBrowser.clear()
        self.last_message_time = 0

    def goToRegistration(self):
        self.stackedWidget.setCurrentIndex(1)

    def goToLogin(self):
        self.stackedWidget.setCurrentIndex(0)

    def clearCredentials(self):
        self.passwordLine1.clear()
        self.loginLine1.clear()
        self.passwordLine2.clear()
        self.loginLine2.clear()
        self.password = None

    def showAboutBox(self):
        QMessageBox.information(self, 'About', self.message_box_text["about"])

    def showContactsBox(self):
        QMessageBox.information(self, 'Contacts', self.message_box_text["contacts"])

    def showServerOffBox(self):
        QMessageBox.critical(self, 'Opsss...', self.message_box_text["serverIsOff"])
        self.goToLogin()

    def showShortcutsBox(self):
        QMessageBox.information(self, 'Shortcuts', self.message_box_text["shortcuts"])

    def showCommandsBox(self):
        output = helpClient(self.client_commands, self.server_commands, [])
        output = output.replace('=', '')
        QMessageBox.information(self, 'Commands', output)

    def signUpUser(self):
        self.loginError2.setText(self._translate("Messenger", self.warning_messages['emptyStr']))
        self.passwordError2.setText(self._translate("Messenger", self.warning_messages['emptyStr']))
        self.loginLine2.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine2.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine2.text()
        self.password = self.passwordLine2.text()

        if not self.username:
            if not self.password:
                self.loginError2.setText(self._translate("Messenger", self.warning_messages['loginRequired']))
                self.passwordError2.setText(self._translate("Messenger", self.warning_messages['passwordRequired']))
                self.loginLine2.setStyleSheet("border: 1px solid red")
                self.passwordLine2.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError2.setText(self._translate("Messenger", self.warning_messages['loginRequired']))
                self.loginLine2.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError2.setText(self._translate("Messenger", self.warning_messages['passwordRequired']))
                self.passwordLine2.setStyleSheet("border: 1px solid red")
                return

        if not self.username.isalnum():
            self.loginError2.setText(self._translate("Messenger", self.warning_messages['notAlphanumeric']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return

        try:
            response = post(
                f'http://{self.server_IP}/signup',
                auth=(self.username, self.password),
                verify=False
            )
        except exceptions.RequestException as e:
            print(e)
            self.showServerOffBox()
            self.clearCredentials()
            return

        if response.json()['loginOutOfRange']:
            self.loginError2.setText(self._translate("Messenger", self.warning_messages['loginOutOfRange']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return
        elif response.json()['passwordOutOfRange']:
            self.passwordError2.setText(self._translate("Messenger", self.warning_messages['passwordOutOfRange']))
            self.passwordError2.adjustSize()
            self.passwordLine2.setStyleSheet("border: 1px solid red")
            return
        elif not response.json()['ok']:
            self.loginError2.setText(self._translate("Messenger", self.warning_messages['registered']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return

        self.getServerCommands()
        self.stackedWidget.setCurrentIndex(2)
        self.actionLogout.setEnabled(True)
        self.actionCommands.setEnabled(True)
        self.clearCredentials()

    def loginUser(self):
        self.loginError1.setText(self._translate("Messenger", self.warning_messages['emptyStr']))
        self.passwordError1.setText(self._translate("Messenger", self.warning_messages['emptyStr']))
        self.loginLine1.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine1.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine1.text()
        self.password = self.passwordLine1.text()

        if not self.username:
            if not self.password:
                self.loginError1.setText(self._translate("Messenger", self.warning_messages['loginRequired']))
                self.passwordError1.setText(self._translate("Messenger", self.warning_messages['passwordRequired']))
                self.loginLine1.setStyleSheet("border: 1px solid red")
                self.passwordLine1.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError1.setText(self._translate("Messenger", self.warning_messages['loginRequired']))
                self.loginLine1.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError1.setText(self._translate("Messenger", self.warning_messages['passwordRequired']))
                self.passwordLine1.setStyleSheet("border: 1px solid red")
                return

        try:
            response = post(
                f'http://{self.server_IP}/auth',
                auth=(self.username, self.password),
                verify=False
            )
        except exceptions.RequestException as e:
            print(e)
            self.showServerOffBox()
            self.clearCredentials()
            return

        if not response.json()['exist']:
            self.loginError1.setText(self._translate("Messenger", self.warning_messages['invalidLogin']))
            self.loginLine1.setStyleSheet("border: 1px solid red")
            return
        if not response.json()['match']:
            self.passwordError1.setText(self._translate("Messenger", self.warning_messages['invalidPassword']))
            self.passwordLine1.setStyleSheet("border: 1px solid red")
            return
        if response.json()['banned']:
            self.loginError1.setText(self._translate("Messenger", self.warning_messages['banned']))
            self.loginLine1.setStyleSheet("border: 1px solid red")
            return

        self.getServerCommands()
        self.stackedWidget.setCurrentIndex(2)
        self.actionLogout.setEnabled(True)
        self.actionCommands.setEnabled(True)
        self.clearCredentials()

    def getServerCommands(self):
        try:
            response = post(
                f'http://{self.server_IP}/command',
                json={"username": self.username, "command": 'help'}, verify=False
            )
        except exceptions.RequestException as e:
            print(e)
            self.clearUserData()
            self.showServerOffBox()
            return

        if not response.json()['ok']:
            self.addText(response.json()['output'] + "<br>")
            self.plainTextEdit.clear()
            return

        self.server_commands = response.json()['output']

        for cmd in self.server_commands:
            if cmd['name'] != 'help': self.run_server_command[f"{cmd['name']}"] = globals()[cmd['name']]

    def send(self):
        text = self.plainTextEdit.toPlainText()
        text = text.strip()

        text = text.replace('</', '')
        text = text.replace('<', '')
        text = text.replace('>', '')

        if len(text) > self.max_text_len:
            text = text[:self.max_text_len]

        if not text:
            return
        elif text.startswith('/'):
            self.sendCommand(text[1:])
        else:
            self.sendMessage(text)

    def sendMessage(self, text):
        try:
            post(
                f'http://{self.server_IP}/send',
                json={"username": self.username, "text": text},
                verify=False
            )
        except exceptions.RequestException as e:
            print(e)
            self.clearUserData()
            self.showServerOffBox()
            return

        self.plainTextEdit.clear()
        self.plainTextEdit.repaint()

    def sendCommand(self, cmd_string):
        command = cmd_string.split()[0]
        args = cmd_string.split()[1:] if len(cmd_string) > 1 else None

        if command in [cmd['name'] for cmd in self.client_commands]:
            self.run_client_command.get(command)()
            self.plainTextEdit.clear()
            return

        elif command not in [cmd['name'] for cmd in self.server_commands]:
            self.addText(f"<b>Error:</b> Command '/{command}' not found.<br>"
                         f"Try '/help' to list all available commands :)<br>")
            self.plainTextEdit.clear()
            return

        elif command == 'help':
            output = helpClient(self.client_commands, self.server_commands, args)
            self.addText(output)
            self.plainTextEdit.clear()
            return

        try:
            response = post(
                f'http://{self.server_IP}/command',
                json={"username": self.username, "command": cmd_string}, verify=False
            )
        except exceptions.RequestException as e:
            print(e)
            self.clearUserData()
            self.showServerOffBox()
            return

        if not response.json()['ok']:
            self.addText("<b>Error:</b> " + response.json()['output'] + "<br>")
            self.plainTextEdit.clear()
            return

        run_command = self.run_server_command.get(command)
        output = run_command(response.json()['output'], args)

        self.addText(output)
        self.plainTextEdit.clear()
        self.plainTextEdit.repaint()

    def getUpdates(self):
        if not self.stackedWidget.currentIndex() == 2:
            return

        try:
            response = get(
                f'http://{self.server_IP}/messages',
                params={'after': self.last_message_time},
                verify=False
            )
            data = response.json()
        except exceptions.RequestException as e:
            print(e)
            self.clearUserData()
            self.showServerOffBox()
            return

        for message in data['messages']:
            # float -> datetime
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')

            self.addText(message['username'] + ' ' + beauty_time)
            self.addText(message['text'] + "<br>")
            self.last_message_time = message['time']

    def getStatus(self):
        if self.stackedWidget.currentIndex() == 2:
            return

        try:
            response = get(
                f'http://{self.server_IP}/status',
                verify=False
            )
            status = response.json()
        except exceptions.RequestException as e:
            self.serverStatus.setText(self._translate("Messenger", '<p style="font-size:12px">'
                                                                   '<img src="Images/server-is-off.png"> Offline</p>'))
            tool_tip = f"Server isn't working<br>" \
                       f"For more information please contact with developer using 'Contacts' tab in 'Help' menu above"
            self.serverStatus.setToolTip(tool_tip)
            return

        self.serverStatus.setText(self._translate("Messenger", '<p style="font-size:12px">'
                                                               '<img src="Images/server-is-on.png"> Online</p>'))
        tool_tip = f"Server is working<br>" \
                   f"Users online: {status['users_online']}<br>" \
                   f"Date and time: {status['time']}<br>" \
                   f"Registered users: {status['users_count']}<br>" \
                   f"Written messages: {status['messages_count']}"
        self.serverStatus.setToolTip(tool_tip)

    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()


app = QtWidgets.QApplication([])
window = MessengerWindow()
app.setStyleSheet(load_stylesheet())
window.show()
app.exec_()
