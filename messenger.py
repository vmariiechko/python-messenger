from datetime import datetime
import requests
from PyQt5 import QtWidgets, QtCore
import clientui


class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sendButton.pressed.connect(self.sendMessage)
        self.loginButton.pressed.connect(self.loginUser)
        self.textEdit.installEventFilter(self)
        self.last_message_time = 0
        self.username = None
        self.password = None
        self.errorMessages = {
            "emptyStr": '<html><head/><body><p><br/></p></body></html>',
            "loginRequired": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Login is '
                             'required</span></p></body></html>',
            "passwordRequired": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Password is '
                                'required</span></p></body></html> ',
            "wrongPassword": '<html><head/><body><p><span style=" font-style:italic; color:#ef2929;">Password '
                             'doesn\'t match</span></p></body></html> '
        }
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
            if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus():
                self.sendMessage()
                return True
        return super().eventFilter(obj, event)

    def loginUser(self):
        _translate = QtCore.QCoreApplication.translate
        self.loginError.setText(_translate("Messenger", self.errorMessages['emptyStr']))
        self.passwordError.setText(_translate("Messenger", self.errorMessages['emptyStr']))
        self.loginLine.setStyleSheet("border: 1px solid #B8B5B2")
        self.passwordLine.setStyleSheet("border: 1px solid #B8B5B2")
        self.username = self.loginLine.text()
        self.password = self.passwordLine.text()

        if not self.username:
            if not self.password:
                self.loginError.setText(_translate("Messenger", self.errorMessages['loginRequired']))
                self.passwordError.setText(_translate("Messenger", self.errorMessages['passwordRequired']))
                self.loginLine.setStyleSheet("border: 1px solid red")
                self.passwordLine.setStyleSheet("border: 1px solid red")
                return
            else:
                self.loginError.setText(_translate("Messenger", self.errorMessages['loginRequired']))
                self.loginLine.setStyleSheet("border: 1px solid red")
                return
        else:
            if not self.password:
                self.passwordError.setText(_translate("Messenger", self.errorMessages['passwordRequired']))
                self.passwordLine.setStyleSheet("border: 1px solid red")
                return

        response = requests.post(
            'http://127.0.0.1:5000/auth',
            json={"username": self.username, "password": self.password}
        )
        if not response.json()['ok']:
            self.passwordError.setText(_translate("Messenger", self.errorMessages['wrongPassword']))
            self.passwordLine.setStyleSheet("border: 1px solid red")
            return

        self.stackedWidget.setCurrentIndex(1)

    def sendMessage(self):
        text = self.textEdit.toPlainText()

        if not text:
            self.addText('ERROR: text is empty!')
            self.addText('')
            return

        response = requests.post(   # todo response unused
            'http://127.0.0.1:5000/send',
            json={"username": self.username, "text": text}
        )

        self.textEdit.clear()
        self.textEdit.repaint()

    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()

    def getUpdates(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.last_message_time}
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
            self.addText(message['text'])
            self.addText('')
            self.last_message_time = message['time']


app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()
app.exec_()
