from datetime import datetime
import requests
from PyQt5 import QtWidgets, QtCore
import clientui
from clicklabel import clickable


class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        self.sendButton.pressed.connect(self.sendMessage)
        self.signUpButton.pressed.connect(self.signUpUser)
        self.loginButton.pressed.connect(self.loginUser)
        self.textEdit.installEventFilter(self)
        self.last_message_time = 0
        self.username = None
        self.password = None
        self.errorMessages = {
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
                                  'must be between 4 and 20 in length</span></p></body></html> '

        }
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)
        clickable(self.signUpLabel).connect(self.goToRegistration)
        clickable(self.loginLabel).connect(self.goToLogin)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
            if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus():
                self.sendMessage()
                return True
        return super().eventFilter(obj, event)

    def goToRegistration(self):
        self.stackedWidget.setCurrentIndex(1)

    def goToLogin(self):
        self.stackedWidget.setCurrentIndex(0)

    def signUpUser(self):
        self.loginError2.setText(self._translate("Messenger", self.errorMessages['emptyStr']))
        self.passwordError2.setText(self._translate("Messenger", self.errorMessages['emptyStr']))
        self.loginLine2.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine2.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine2.text()
        self.password = self.passwordLine2.text()

        if not self.username:
            if not self.password:
                self.loginError2.setText(self._translate("Messenger", self.errorMessages['loginRequired']))
                self.passwordError2.setText(self._translate("Messenger", self.errorMessages['passwordRequired']))
                self.loginLine2.setStyleSheet("border: 1px solid red")
                self.passwordLine2.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError2.setText(self._translate("Messenger", self.errorMessages['loginRequired']))
                self.loginLine2.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError2.setText(self._translate("Messenger", self.errorMessages['passwordRequired']))
                self.passwordLine2.setStyleSheet("border: 1px solid red")
                return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/signup',
                json={"username": self.username, "password": self.password}
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit  # todo warning screen about error

        if response.json()['loginOutOfRange']:
            self.loginError2.setText(self._translate("Messenger", self.errorMessages['loginOutOfRange']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return
        elif response.json()['passwordOutOfRange']:
            self.passwordError2.setText(self._translate("Messenger", self.errorMessages['passwordOutOfRange']))
            self.passwordError2.adjustSize()
            self.passwordLine2.setStyleSheet("border: 1px solid red")
            return
        elif not response.json()['ok']:
            self.loginError2.setText(self._translate("Messenger", self.errorMessages['registered']))
            self.loginError2.adjustSize()
            self.loginLine2.setStyleSheet("border: 1px solid red")
            return

        self.stackedWidget.setCurrentIndex(2)

    def loginUser(self):
        self.loginError1.setText(self._translate("Messenger", self.errorMessages['emptyStr']))
        self.passwordError1.setText(self._translate("Messenger", self.errorMessages['emptyStr']))
        self.loginLine1.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine1.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine1.text()
        self.password = self.passwordLine1.text()

        if not self.username:
            if not self.password:
                self.loginError1.setText(self._translate("Messenger", self.errorMessages['loginRequired']))
                self.passwordError1.setText(self._translate("Messenger", self.errorMessages['passwordRequired']))
                self.loginLine1.setStyleSheet("border: 1px solid red")
                self.passwordLine1.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError1.setText(self._translate("Messenger", self.errorMessages['loginRequired']))
                self.loginLine1.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError1.setText(self._translate("Messenger", self.errorMessages['passwordRequired']))
                self.passwordLine1.setStyleSheet("border: 1px solid red")
                return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/auth',
                json={"username": self.username, "password": self.password}
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit  # todo warning screen about error

        if not response.json()['exist']:
            self.loginError1.setText(self._translate("Messenger", self.errorMessages['invalidLogin']))
            self.loginLine1.setStyleSheet("border: 1px solid red")
            return
        if not response.json()['match']:
            self.passwordError1.setText(self._translate("Messenger", self.errorMessages['invalidPassword']))
            self.passwordLine1.setStyleSheet("border: 1px solid red")
            return

        self.stackedWidget.setCurrentIndex(2)

    def sendMessage(self):
        text = self.textEdit.toPlainText()
        text = text.strip()

        if not text:
            return

        try:
            requests.post(
                'http://127.0.0.1:5000/send',
                json={"username": self.username, "text": text}
            )
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit  # todo warning screen about error

        self.textEdit.clear()
        self.textEdit.repaint()

    def getUpdates(self):
        if not self.stackedWidget.currentIndex() == 2:
            return

        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.last_message_time}
            )
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit  # todo warning screen about error

        for message in data['messages']:
            # float -> datetime
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
            self.addText(message['username'] + ' ' + beauty_time)
            self.addText(message['text'])
            self.addText('')
            self.last_message_time = message['time']

    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()


app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()
app.exec_()
