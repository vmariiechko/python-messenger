from requests import get, post, exceptions
from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont
from qtwidgets import PasswordEdit

from client_commands import (help_client, online, status, myself, reg, role, ban, unban)
from client_content import (get_warning_messages, get_client_commands, get_message_box_text, get_message_style)
from click_label import clickable
from client_ui import Ui_Messenger
from preferences import Preferences
from style_sheet import load_stylesheet


class Messenger(QtWidgets.QMainWindow, Ui_Messenger):
    """
    The messenger object acts as the main object and is managed by client.

    Shows UI and is responsible for UX.
    UI is separated on 3 main parts, which have their indexes: 0 - Login form, 1 - Registration form, 2 - Chat.
    Every 5 seconds requests server status.
    Every second shows new messages, if user logged in.
    Under main label "Python Messenger" there is server status, which displays whether server is working,
    if yes, you can hover on it to see full server status.
    In case of disconnection from server it'll show server-off message and navigate to login form.
    It's possible to change server IP address in preferences menu.

    :param translate: properly shows all content
    :param password_line1: input line with icons to show/hide password entries on login form
    :param password_line2: input line with icons to show/hide password entries on registration form
    :param username: user nickname string
    :param password: user password string
    :param last_message_time: last time of getting messages, defaults to 0
    :param max_text_len: maximum text message length to send in chat, defaults to 250
    :param server_IP: server IPv4 string
    :param message_style: style for messages defined in :func:`get_message_style`
    :param warning_messages: dict of warning messages defined in :func:`get_warning_messages`
    :param message_box_text: dict of content for message box defined in :func:`get_message_box_text`
    :param client_commands: list of dicts with client-side commands defined in :func:`get_client_commands`
    :param run_client_command: dict, where key is the name of client command and value is the function of this command
    :param server_commands: list of dicts with server-side commands defined in :func:`get_server_commands`
    :param run_server_command: dict, where key is the name of server command and value is the function of this command
    :param timer_get_messages: timer, which every second runs :func:`get_messages`
    :param timer_get_status: timer, which every 5 seconds runs :func:`get_status`
    """

    def __init__(self, parent=None):
        """Initialize messenger object."""

        super().__init__(parent)
        self.setupUi(self)
        self.translate = QtCore.QCoreApplication.translate

        self.password_line1 = PasswordEdit(True, self.login_page)
        self.password_line2 = PasswordEdit(True, self.registration_page)
        self.modify_password_lines()

        # Connect buttons to the methods.
        self.send_button.pressed.connect(self.send)
        self.sign_up_button.pressed.connect(self.sign_up_user)
        self.login_button.pressed.connect(self.login_user)

        # Connect actions to the methods.
        self.action_shortcuts.triggered.connect(self.show_shortcuts_box)
        self.action_commands.triggered.connect(self.show_commands_box)
        self.action_about.triggered.connect(self.show_about_box)
        self.action_contacts.triggered.connect(self.show_contacts_box)
        self.action_preferences.triggered.connect(self.open_preferences_window)
        self.action_logout.triggered.connect(self.logout)
        self.action_close.triggered.connect(self.close)

        # Filter shortcuts and text overflow.
        self.plain_text_edit.installEventFilter(self)

        self.username = None
        self.password = None
        self.last_message_time = 0
        self.max_text_len = 250
        self.server_IP = '0.0.0.0:9000'

        # Load client content.
        self.message_style = get_message_style()
        self.warning_messages = get_warning_messages()
        self.message_box_text = get_message_box_text()

        # Load commands.
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
        """
        Filters Enter key press and message text length.

        If Enter key pressed, sends user's message.
        If length of message is above maximum, doesn't allow writing.
        """

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
        """
        Shows question message box for acception or ignoring to close the messenger.

        Asks user does he really wants to close the messenger, if yes,
        than marks logout of user and closes the messenger.
        Otherwise, ignores closing messenger event.

        :param event: event to close the messenger
        """

        reply = QMessageBox.question(self, 'Quit', self.message_box_text["close"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        # User closes the messenger and is logged in.
        if reply == QMessageBox.Yes and self.stacked_widget.currentIndex() == 2:
            try:
                post(
                    f'http://{self.server_IP}/logout',
                    json={"username": self.username}, verify=False
                )
            except exceptions.RequestException as e:
                raise SystemExit

            event.accept()

        # User closes the messenger and is logged out.
        elif reply == QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()

    def logout(self):
        """
        Shows question message box for acception or ignoring to log out from account.

        Asks user does he really wants to log out, if yes,
        than marks logout and navigates to login form.
        Otherwise, ignores logout event.
        """

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
        """Modifies and appears password lines."""

        geometry = QtCore.QRect(60, 200, 291, 41)
        font = QFont()
        font.setPointSize(14)

        self.password_line1.setGeometry(geometry)
        self.password_line1.setFont(font)
        self.password_line1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line1.setObjectName("password_line1")
        self.password_line1.setPlaceholderText(self.translate("Messenger", "Password"))

        self.password_line2.setGeometry(geometry)
        self.password_line2.setFont(font)
        self.password_line2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line2.setObjectName("password_line2")
        self.password_line2.setPlaceholderText(self.translate("Messenger", "Enter Your Password"))

    def open_preferences_window(self):
        """Opens settings window."""

        settings = Preferences(self)
        if settings.exec():
            self.server_IP = settings.server_IP.text()

    def clear_user_data(self):
        """Clears user data after logout."""

        self.username = None
        self.plain_text_edit.clear()
        self.text_browser.clear()
        self.last_message_time = 0

    def reload(self):
        """Reloads all messages and deletes commands output."""

        self.text_browser.clear()
        self.last_message_time = 0

    def go_to_registration_form(self):
        """Navigates to registration menu."""

        self.stacked_widget.setCurrentIndex(1)

    def go_to_login_form(self):
        """Navigates to login menu."""

        self.stacked_widget.setCurrentIndex(0)

    def go_to_chat(self):
        """Navigates to chat."""

        self.get_server_commands()
        self.stacked_widget.setCurrentIndex(2)
        self.action_logout.setEnabled(True)
        self.action_commands.setEnabled(True)
        self.plain_text_edit.setFocus()
        self.clear_credentials()

    def clear_credentials(self):
        """Clears login and password lines after log in or sign up."""

        self.password_line1.clear()
        self.login_line1.clear()
        self.password_line2.clear()
        self.login_line2.clear()
        self.password = None

    def show_about_box(self):
        """Shows message box with content about messenger."""

        QMessageBox.information(self, 'About', self.message_box_text["about"])

    def show_contacts_box(self):
        """Shows message box with contacts information."""

        QMessageBox.information(self, 'Contacts', self.message_box_text["contacts"])

    def show_server_off_box(self):
        """Shows message box about server off information."""

        QMessageBox.critical(self, 'Opsss...', self.message_box_text["server_is_off"])
        self.go_to_login_form()

    def show_shortcuts_box(self):
        """Shows message box with shortcuts."""

        QMessageBox.information(self, 'Shortcuts', self.message_box_text["shortcuts"])

    def show_commands_box(self):
        """Shows message box with available commands."""

        output = help_client(self.client_commands, self.server_commands, [])
        output = output.replace('=', '')
        QMessageBox.information(self, 'Commands', output)

    def sign_up_user(self):
        """
        Registers user.

        Verifies correctness of login and password input.
        Sends request to sign up user.
        """

        # Clear registration form.
        self.login_error2.setText(self.translate("Messenger", self.warning_messages['empty_str']))
        self.password_error2.setText(self.translate("Messenger", self.warning_messages['empty_str']))
        self.login_line2.setStyleSheet("border: 1px solid #B8B5B2")
        self.password_line2.setStyleSheet("border: 1px solid #B8B5B2")

        self.username = self.login_line2.text()
        self.password = self.password_line2.text()

        # Check that form isn't empty.
        if not self.username:
            if not self.password:
                self.login_error2.setText(self.translate("Messenger", self.warning_messages['login_required']))
                self.password_error2.setText(self.translate("Messenger", self.warning_messages['password_required']))
                self.login_line2.setStyleSheet("border: 1px solid red")
                self.password_line2.setStyleSheet("border: 1px solid red")
                return
            else:
                self.login_error2.setText(self.translate("Messenger", self.warning_messages['login_required']))
                self.login_line2.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.password_error2.setText(self.translate("Messenger", self.warning_messages['password_required']))
                self.password_line2.setStyleSheet("border: 1px solid red")
                return

        if not self.username.isalnum():
            self.login_error2.setText(self.translate("Messenger", self.warning_messages['not_alphanumeric']))
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

        # Process bad request.
        if response.json()['login_out_of_range']:
            self.login_error2.setText(self.translate("Messenger", self.warning_messages['login_out_of_range']))
            self.login_error2.adjustSize()
            self.login_line2.setStyleSheet("border: 1px solid red")
            return
        elif response.json()['password_out_of_range']:
            self.password_error2.setText(self.translate("Messenger", self.warning_messages['password_out_of_range']))
            self.password_error2.adjustSize()
            self.password_line2.setStyleSheet("border: 1px solid red")
            return
        elif not response.json()['ok']:
            self.login_error2.setText(self.translate("Messenger", self.warning_messages['registered']))
            self.login_error2.adjustSize()
            self.login_line2.setStyleSheet("border: 1px solid red")
            return

        self.go_to_chat()

    def login_user(self):
        """
        Allows user to log in.

        Verifies correctness of login and password input.
        Sends request to authenticate user.
        """

        # Clear login form.
        self.login_error1.setText(self.translate("Messenger", self.warning_messages['empty_str']))
        self.password_error1.setText(self.translate("Messenger", self.warning_messages['empty_str']))
        self.login_line1.setStyleSheet("border: 1px solid #B8B5B2")
        self.password_line1.setStyleSheet("border: 1px solid #B8B5B2")

        self.username = self.login_line1.text()
        self.password = self.password_line1.text()

        # Check that form isn't empty.
        if not self.username:
            if not self.password:
                self.login_error1.setText(self.translate("Messenger", self.warning_messages['login_required']))
                self.password_error1.setText(self.translate("Messenger", self.warning_messages['password_required']))
                self.login_line1.setStyleSheet("border: 1px solid red")
                self.password_line1.setStyleSheet("border: 1px solid red")
                return
            else:
                self.login_error1.setText(self.translate("Messenger", self.warning_messages['login_required']))
                self.login_line1.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.password_error1.setText(self.translate("Messenger", self.warning_messages['password_required']))
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

        # Process bad request.
        if not response.json()['exist']:
            self.login_error1.setText(self.translate("Messenger", self.warning_messages['invalid_login']))
            self.login_line1.setStyleSheet("border: 1px solid red")
            return
        if not response.json()['match']:
            self.password_error1.setText(self.translate("Messenger", self.warning_messages['invalid_password']))
            self.password_line1.setStyleSheet("border: 1px solid red")
            return
        if response.json()['banned']:
            self.login_error1.setText(self.translate("Messenger", self.warning_messages['banned']))
            self.login_line1.setStyleSheet("border: 1px solid red")
            return

        self.go_to_chat()

    def get_server_commands(self):
        """Sends request to get available server-side commands for user."""

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

        # Connect command name with function.
        for cmd in self.server_commands:
            if cmd['name'] != 'help': self.run_server_command[f"{cmd['name']}"] = globals()[cmd['name']]

    def send(self):
        """Separates and directs messages & commands to relevant function."""

        self.plain_text_edit.setFocus()

        text = self.plain_text_edit.toPlainText()
        text = text.strip()

        # Validate text don't execute HTML.
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
        """
        Stores message on the server.

        :param text: text of message
        """

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
        """
        Executes command.

        If it's client-side command, executes directly from client.
        If it's server-side command, sends command to execute
        on the server and processes the output.

        :param cmd_string: command with parameters to execute
        """

        command = cmd_string.split()[0]
        args = cmd_string.split()[1:] if len(cmd_string) > 1 else None

        # Run client-side command.
        if command in [cmd['name'] for cmd in self.client_commands]:
            self.run_client_command.get(command)()
            self.plain_text_edit.clear()
            return

        # Invalid command name.
        elif command not in [cmd['name'] for cmd in self.server_commands]:
            self.show_text(f"<b>Error:</b> Command '/{command}' not found.<br>"
                           f"Try '/help' to list all available commands :)<br>")
            self.plain_text_edit.clear()
            return

        # Process 'help' command.
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

        # Assign command function & run it with output from server.
        run_command = self.run_server_command.get(command)
        output = run_command(response.json()['output'], args)

        self.show_text(output)
        self.plain_text_edit.clear()
        self.plain_text_edit.repaint()

    def get_messages(self):
        """Sends request to get new messages and appears them in style."""

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

        # Generate message.
        for message in data['messages']:
            # float -> datetime.
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%d/%m %H:%M:%S')

            # User will see his messages from the right side.
            if message['username'] == self.username:
                self.show_text(self.message_style['begin'] + beauty_time + ' ' + message['username']
                               + self.message_style['middle'] + message['text'] + self.message_style['end'])
                self.last_message_time = message['time']

            else:
                self.show_text(message['username'] + ' ' + beauty_time)
                self.show_text(message['text'] + "<br>")
                self.last_message_time = message['time']

    def get_status(self):
        """Sends request to get server status."""

        try:
            response = get(
                f'http://{self.server_IP}/status',
                verify=False
            )
            status = response.json()

        # Server is off.
        except exceptions.RequestException as e:
            self.server_status.setText(self.translate("Messenger", '<p style="font-size:12px">'
                                                                    '<img src="images/server-is-off.png"> Offline</p>'))
            tool_tip = f"Can't connect to the server<br>" \
                       f"Maybe server isn't run or you've entered an invalid IP address in Preferences"
            self.server_status.setToolTip(tool_tip)
            return

        # Server is on.
        self.server_status.setText(self.translate("Messenger", '<p style="font-size:12px">'
                                                                '<img src="images/server-is-on.png"> Online</p>'))
        tool_tip = f"Server is working<br>" \
                   f"Users online: {status['users_online']}<br>" \
                   f"Date and time: {status['time']}<br>" \
                   f"Registered users: {status['users_count']}<br>" \
                   f"Written messages: {status['messages_count']}"
        self.server_status.setToolTip(tool_tip)

    def show_text(self, text):
        """Shows given text in messenger chat."""

        self.text_browser.append(text)
        self.text_browser.repaint()


app = QtWidgets.QApplication([])
window = Messenger()
app.setStyleSheet(load_stylesheet())
window.show()
app.exec_()
