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

        self.password_line1 = PasswordEdit(True, self.login_page)
        self.password_line2 = PasswordEdit(True, self.registration_page)
        self.modify_password_lines()

        self.send_button.pressed.connect(self.send)
        self.sign_up_button.pressed.connect(self.sign_up_user)
        self.login_button.pressed.connect(self.login_user)

        self.action_shortcuts.triggered.connect(self.show_shortcuts_box)
        self.action_commands.triggered.connect(self.show_commands_box)
        self.action_about.triggered.connect(self.show_about_box)
        self.action_contacts.triggered.connect(self.show_contacts_box)
        self.action_preferences.triggered.connect(self.open_preferences_window)
        self.action_logout.triggered.connect(self.logout)
        self.action_close.triggered.connect(self.close)

        self.plain_text_edit.installEventFilter(self)

        self.username = None
        self.password = None
        self.last_message_time = 0
        self.max_text_len = 250
        self.server_IP = '127.0.0.1:5000'

        self.message_style = get_message_style()
        self.warning_messages = get_warning_messages()
        self.message_box_text = get_message_box_text()

        self.client_commands = get_client_commands()
        self.run_client_command = {'close': self.close,
                                   'logout': self.logout,
                                   'reload': self.reload}
        self.server_commands = []
        self.run_server_command = {}

        self.timer_get_messages = QtCore.QTimer()
        self.timer_get_messages.timeout.connect(self.get_messages)
        self.timer_get_messages.start(1000)

        self.timer_get_status = QtCore.QTimer()
        self.timer_get_status.timeout.connect(self.get_status)
        self.timer_get_status.start(5000)

        clickable(self.go_to_sign_up).connect(self.go_to_registration_form)
        clickable(self.go_to_login).connect(self.go_to_login_form)

        self.get_status()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.plain_text_edit:
            text = self.plain_text_edit.toPlainText()

            if event.key() == QtCore.Qt.Key_Return and self.plain_text_edit.hasFocus():
                self.send()
                return True

            elif len(text) > self.max_text_len:
                text = text[:self.max_text_len]
                self.plain_text_edit.setPlainText(text)

                cursor = self.plain_text_edit.textCursor()
                cursor.setPosition(self.max_text_len)
                self.plain_text_edit.setTextCursor(cursor)
                return True

        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', self.message_box_text["close"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes and self.stacked_widget.currentIndex() == 2:
            try:
                post(
                    f'http://{self.server_IP}/logout',
                    json={"username": self.username}, verify=False
                )
            except exceptions.RequestException as e:
                raise SystemExit

            event.accept()

        elif reply == QMessageBox.Yes:
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
                self.show_server_off_box()
                self.clear_user_data()
                return

            self.go_to_login_form()
            self.clear_user_data()
            self.action_logout.setEnabled(False)
            self.action_commands.setEnabled(False)
        else:
            return

    def modify_password_lines(self):
        geometry = QtCore.QRect(60, 200, 291, 41)
        font = QFont()
        font.setPointSize(14)

        self.password_line1.setGeometry(geometry)
        self.password_line1.setFont(font)
        self.password_line1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line1.setObjectName("password_line1")
        self.password_line1.setPlaceholderText(self._translate("Messenger", "Password"))

        self.password_line2.setGeometry(geometry)
        self.password_line2.setFont(font)
        self.password_line2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line2.setObjectName("password_line2")
        self.password_line2.setPlaceholderText(self._translate("Messenger", "Enter Your Password"))

    def open_preferences_window(self):
        dlg = PreferencesWindow(self)
        if dlg.exec():
            self.server_IP = dlg.server_IP.text()

    def clear_user_data(self):
        self.username = None
        self.plain_text_edit.clear()
        self.text_browser.clear()
        self.last_message_time = 0

    def reload(self):
        self.text_browser.clear()
        self.last_message_time = 0

    def go_to_registration_form(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_login_form(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_chat(self):
        self.get_server_commands()
        self.stacked_widget.setCurrentIndex(2)
        self.action_logout.setEnabled(True)
        self.action_commands.setEnabled(True)
        self.plain_text_edit.setFocus()
        self.clear_credentials()

    def clear_credentials(self):
        self.password_line1.clear()
        self.login_line1.clear()
        self.password_line2.clear()
        self.login_line2.clear()
        self.password = None

    def show_about_box(self):
        QMessageBox.information(self, 'About', self.message_box_text["about"])

    def show_contacts_box(self):
        QMessageBox.information(self, 'Contacts', self.message_box_text["contacts"])

    def show_server_off_box(self):
        QMessageBox.critical(self, 'Opsss...', self.message_box_text["server_is_off"])
        self.go_to_login_form()

    def show_shortcuts_box(self):
        QMessageBox.information(self, 'Shortcuts', self.message_box_text["shortcuts"])

    def show_commands_box(self):
        output = help_client(self.client_commands, self.server_commands, [])
        output = output.replace('=', '')
        QMessageBox.information(self, 'Commands', output)

    def sign_up_user(self):
        self.login_error2.setText(self._translate("Messenger", self.warning_messages['empty_str']))
        self.password_error2.setText(self._translate("Messenger", self.warning_messages['empty_str']))
        self.login_line2.setStyleSheet("border: 1px solid #B8B5B2")
        self.password_line2.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.login_line2.text()
        self.password = self.password_line2.text()

        if not self.username:
            if not self.password:
                self.login_error2.setText(self._translate("Messenger", self.warning_messages['login_required']))
                self.password_error2.setText(self._translate("Messenger", self.warning_messages['password_required']))
                self.login_line2.setStyleSheet("border: 1px solid red")
                self.password_line2.setStyleSheet("border: 1px solid red")
                return
            else:
                self.login_error2.setText(self._translate("Messenger", self.warning_messages['login_required']))
                self.login_line2.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.password_error2.setText(self._translate("Messenger", self.warning_messages['password_required']))
                self.password_line2.setStyleSheet("border: 1px solid red")
                return

        if not self.username.isalnum():
            self.login_error2.setText(self._translate("Messenger", self.warning_messages['not_alphanumeric']))
            self.login_error2.adjustSize()
            self.login_line2.setStyleSheet("border: 1px solid red")
            return

        try:
            response = post(
                f'http://{self.server_IP}/sign_up',
                auth=(self.username, self.password),
                verify=False
            )
        except exceptions.RequestException as e:
            self.show_server_off_box()
            self.clear_credentials()
            return

        if response.json()['login_out_of_range']:
            self.login_error2.setText(self._translate("Messenger", self.warning_messages['login_out_of_range']))
            self.login_error2.adjustSize()
            self.login_line2.setStyleSheet("border: 1px solid red")
            return
        elif response.json()['password_out_of_range']:
            self.password_error2.setText(self._translate("Messenger", self.warning_messages['password_out_of_range']))
            self.password_error2.adjustSize()
            self.password_line2.setStyleSheet("border: 1px solid red")
            return
        elif not response.json()['ok']:
            self.login_error2.setText(self._translate("Messenger", self.warning_messages['registered']))
            self.login_error2.adjustSize()
            self.login_line2.setStyleSheet("border: 1px solid red")
            return

        self.go_to_chat()

    def login_user(self):
        self.login_error1.setText(self._translate("Messenger", self.warning_messages['empty_str']))
        self.password_error1.setText(self._translate("Messenger", self.warning_messages['empty_str']))
        self.login_line1.setStyleSheet("border: 1px solid #B8B5B2")
        self.password_line1.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.login_line1.text()
        self.password = self.password_line1.text()

        if not self.username:
            if not self.password:
                self.login_error1.setText(self._translate("Messenger", self.warning_messages['login_required']))
                self.password_error1.setText(self._translate("Messenger", self.warning_messages['password_required']))
                self.login_line1.setStyleSheet("border: 1px solid red")
                self.password_line1.setStyleSheet("border: 1px solid red")
                return
            else:
                self.login_error1.setText(self._translate("Messenger", self.warning_messages['login_required']))
                self.login_line1.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.password_error1.setText(self._translate("Messenger", self.warning_messages['password_required']))
                self.password_line1.setStyleSheet("border: 1px solid red")
                return

        try:
            response = post(
                f'http://{self.server_IP}/auth',
                auth=(self.username, self.password),
                verify=False
            )
        except exceptions.RequestException as e:
            self.show_server_off_box()
            self.clear_credentials()
            return

        if not response.json()['exist']:
            self.login_error1.setText(self._translate("Messenger", self.warning_messages['invalid_login']))
            self.login_line1.setStyleSheet("border: 1px solid red")
            return
        if not response.json()['match']:
            self.password_error1.setText(self._translate("Messenger", self.warning_messages['invalid_password']))
            self.password_line1.setStyleSheet("border: 1px solid red")
            return
        if response.json()['banned']:
            self.login_error1.setText(self._translate("Messenger", self.warning_messages['banned']))
            self.login_line1.setStyleSheet("border: 1px solid red")
            return

        self.go_to_chat()

    def get_server_commands(self):
        try:
            response = post(
                f'http://{self.server_IP}/command',
                json={"username": self.username, "command": 'help'}, verify=False
            )
        except exceptions.RequestException as e:
            self.clear_user_data()
            self.show_server_off_box()
            return

        if not response.json()['ok']:
            self.show_text(response.json()['output'] + "<br>")
            self.plain_text_edit.clear()
            return

        self.server_commands = response.json()['output']

        for cmd in self.server_commands:
            if cmd['name'] != 'help': self.run_server_command[f"{cmd['name']}"] = globals()[cmd['name']]

    def send(self):
        self.plain_text_edit.setFocus()

        text = self.plain_text_edit.toPlainText()
        text = text.strip()

        text = text.replace('</', '')
        text = text.replace('<', '')
        text = text.replace('>', '')

        if len(text) > self.max_text_len:
            text = text[:self.max_text_len]

        if not text:
            return
        elif text.startswith('/'):
            self.send_command(text[1:])
        else:
            self.send_message(text)

    def send_message(self, text):
        try:
            post(
                f'http://{self.server_IP}/send_message',
                json={"username": self.username, "text": text},
                verify=False
            )
        except exceptions.RequestException as e:
            self.clear_user_data()
            self.show_server_off_box()
            return

        self.plain_text_edit.clear()
        self.plain_text_edit.repaint()

    def send_command(self, cmd_string):
        command = cmd_string.split()[0]
        args = cmd_string.split()[1:] if len(cmd_string) > 1 else None

        if command in [cmd['name'] for cmd in self.client_commands]:
            self.run_client_command.get(command)()
            self.plain_text_edit.clear()
            return

        elif command not in [cmd['name'] for cmd in self.server_commands]:
            self.show_text(f"<b>Error:</b> Command '/{command}' not found.<br>"
                           f"Try '/help' to list all available commands :)<br>")
            self.plain_text_edit.clear()
            return

        elif command == 'help':
            output = help_client(self.client_commands, self.server_commands, args)
            self.show_text(output)
            self.plain_text_edit.clear()
            return

        try:
            response = post(
                f'http://{self.server_IP}/command',
                json={"username": self.username, "command": cmd_string}, verify=False
            )
        except exceptions.RequestException as e:
            self.clear_user_data()
            self.show_server_off_box()
            return

        if not response.json()['ok']:
            self.show_text("<b>Error:</b> " + response.json()['output'] + "<br>")
            self.plain_text_edit.clear()
            return

        run_command = self.run_server_command.get(command)
        output = run_command(response.json()['output'], args)

        self.show_text(output)
        self.plain_text_edit.clear()
        self.plain_text_edit.repaint()

    def get_messages(self):
        if not self.stacked_widget.currentIndex() == 2:
            return

        try:
            response = get(
                f'http://{self.server_IP}/get_messages',
                params={'after': self.last_message_time},
                verify=False
            )
            data = response.json()
        except exceptions.RequestException as e:
            self.clear_user_data()
            self.show_server_off_box()
            return

        for message in data['messages']:
            # float -> datetime
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%d/%m %H:%M:%S')

            if message['username'] == self.username:
                self.show_text(self.message_style['begin'] + beauty_time + ' ' + message['username']
                               + self.message_style['middle'] + message['text'] + self.message_style['end'])
                self.last_message_time = message['time']

            else:
                self.show_text(message['username'] + ' ' + beauty_time)
                self.show_text(message['text'] + "<br>")
                self.last_message_time = message['time']

    def get_status(self):
        if self.stacked_widget.currentIndex() == 2:
            return

        try:
            response = get(
                f'http://{self.server_IP}/status',
                verify=False
            )
            status = response.json()
        except exceptions.RequestException as e:
            self.server_status.setText(self._translate("Messenger", '<p style="font-size:12px">'
                                                                    '<img src="Images/server-is-off.png"> Offline</p>'))
            tool_tip = f"Server isn't working<br>" \
                       f"For more information please contact with developer using 'Contacts' tab in 'Help' menu above"
            self.server_status.setToolTip(tool_tip)
            return

        self.server_status.setText(self._translate("Messenger", '<p style="font-size:12px">'
                                                                '<img src="Images/server-is-on.png"> Online</p>'))
        tool_tip = f"Server is working<br>" \
                   f"Users online: {status['users_online']}<br>" \
                   f"Date and time: {status['time']}<br>" \
                   f"Registered users: {status['users_count']}<br>" \
                   f"Written messages: {status['messages_count']}"
        self.server_status.setToolTip(tool_tip)

    def show_text(self, text):
        self.text_browser.append(text)
        self.text_browser.repaint()


app = QtWidgets.QApplication([])
window = MessengerWindow()
app.setStyleSheet(load_stylesheet())
window.show()
app.exec_()
