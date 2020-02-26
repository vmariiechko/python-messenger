from datetime import datetime
import requests
from PyQt5 import QtWidgets, QtCore
import clientui


class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sendButton.pressed.connect(self.sendMessage)
        self.loginButton1.pressed.connect(self.loginUser)
        self.textEdit.installEventFilter(self)
        self.last_message_time = 0
        self.username = None
        self.password = None
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
        self.username = self.loginLine1.text()
        self.password = self.passwordLine1.text()

        response = requests.post(
            'http://127.0.0.1:5000/auth',
            json={"username": self.username, "password": self.password}
        )
        if not response.json()['ok']:
            return

        self.stackedWidget.setCurrentIndex(1)

    def sendMessage(self):
        text = self.textEdit.toPlainText()

        if not self.username:
            self.addText('ERROR: username is empty!')
            self.addText('')
            return
        if not self.password:
            self.addText('ERROR: password is empty!')
            self.addText('')
            return
        if not text:
            self.addText('ERROR: text is empty!')
            self.addText('')
            return

        response = requests.post(
            'http://127.0.0.1:5000/send',
            json={"username": self.username, "password": self.password, "text": text}
        )
        if not response.json()['ok']:
            self.addText('ERROR: Access denied')
            self.addText('')
            return

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
