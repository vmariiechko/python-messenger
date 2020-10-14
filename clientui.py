# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'messenger.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Messenger(object):
    def setupUi(self, Messenger):
        Messenger.setObjectName("Messenger")
        Messenger.resize(410, 610)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/messenger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Messenger.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Messenger)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 70, 410, 511))
        self.stackedWidget.setObjectName("stackedWidget")
        self.Login_page = QtWidgets.QWidget()
        self.Login_page.setObjectName("Login_page")
        self.loginLine1 = QtWidgets.QLineEdit(self.Login_page)
        self.loginLine1.setGeometry(QtCore.QRect(60, 130, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loginLine1.setFont(font)
        self.loginLine1.setText("")
        self.loginLine1.setObjectName("loginLine1")
        self.passwordLine1 = QtWidgets.QLineEdit(self.Login_page)
        self.passwordLine1.setGeometry(QtCore.QRect(60, 200, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passwordLine1.setFont(font)
        self.passwordLine1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine1.setObjectName("passwordLine1")
        self.loginButton = QtWidgets.QPushButton(self.Login_page)
        self.loginButton.setGeometry(QtCore.QRect(140, 260, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.loginButton.setFont(font)
        self.loginButton.setStyleSheet("")
        self.loginButton.setObjectName("loginButton")
        self.loginError1 = QtWidgets.QLabel(self.Login_page)
        self.loginError1.setGeometry(QtCore.QRect(60, 110, 181, 21))
        self.loginError1.setObjectName("loginError1")
        self.passwordError1 = QtWidgets.QLabel(self.Login_page)
        self.passwordError1.setGeometry(QtCore.QRect(60, 180, 181, 21))
        self.passwordError1.setObjectName("passwordError1")
        self.signUpLabel = QtWidgets.QLabel(self.Login_page)
        self.signUpLabel.setGeometry(QtCore.QRect(140, 300, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.signUpLabel.setFont(font)
        self.signUpLabel.setStyleSheet("QLabel:hover#signUpLabel\n"
"{\n"
"   color:blue;\n"
"}")
        self.signUpLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.signUpLabel.setObjectName("signUpLabel")
        self.stackedWidget.addWidget(self.Login_page)
        self.Registration_page = QtWidgets.QWidget()
        self.Registration_page.setObjectName("Registration_page")
        self.loginLine2 = QtWidgets.QLineEdit(self.Registration_page)
        self.loginLine2.setGeometry(QtCore.QRect(60, 130, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loginLine2.setFont(font)
        self.loginLine2.setText("")
        self.loginLine2.setObjectName("loginLine2")
        self.signUpButton = QtWidgets.QPushButton(self.Registration_page)
        self.signUpButton.setGeometry(QtCore.QRect(140, 260, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.signUpButton.setFont(font)
        self.signUpButton.setStyleSheet("")
        self.signUpButton.setObjectName("signUpButton")
        self.passwordLine2 = QtWidgets.QLineEdit(self.Registration_page)
        self.passwordLine2.setGeometry(QtCore.QRect(60, 200, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passwordLine2.setFont(font)
        self.passwordLine2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine2.setObjectName("passwordLine2")
        self.loginLabel = QtWidgets.QLabel(self.Registration_page)
        self.loginLabel.setGeometry(QtCore.QRect(120, 300, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.loginLabel.setFont(font)
        self.loginLabel.setStyleSheet("QLabel:hover#loginLabel\n"
"{\n"
"   color:blue;\n"
"}")
        self.loginLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loginLabel.setObjectName("loginLabel")
        self.loginError2 = QtWidgets.QLabel(self.Registration_page)
        self.loginError2.setGeometry(QtCore.QRect(60, 110, 181, 21))
        self.loginError2.setObjectName("loginError2")
        self.passwordError2 = QtWidgets.QLabel(self.Registration_page)
        self.passwordError2.setGeometry(QtCore.QRect(60, 180, 181, 21))
        self.passwordError2.setObjectName("passwordError2")
        self.stackedWidget.addWidget(self.Registration_page)
        self.Chat_page = QtWidgets.QWidget()
        self.Chat_page.setObjectName("Chat_page")
        self.textBrowser = QtWidgets.QTextBrowser(self.Chat_page)
        self.textBrowser.setGeometry(QtCore.QRect(20, 30, 371, 401))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.sendButton = QtWidgets.QPushButton(self.Chat_page)
        self.sendButton.setGeometry(QtCore.QRect(320, 460, 71, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sendButton.setFont(font)
        self.sendButton.setObjectName("sendButton")
        self.textEdit = QtWidgets.QTextEdit(self.Chat_page)
        self.textEdit.setGeometry(QtCore.QRect(20, 450, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.stackedWidget.addWidget(self.Chat_page)
        self.messengerLabel = QtWidgets.QLabel(self.centralwidget)
        self.messengerLabel.setGeometry(QtCore.QRect(70, 30, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.messengerLabel.setFont(font)
        self.messengerLabel.setObjectName("messengerLabel")
        Messenger.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Messenger)
        self.statusbar.setObjectName("statusbar")
        Messenger.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(Messenger)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 410, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(False)
        self.menuBar.setFont(font)
        self.menuBar.setObjectName("menuBar")
        self.menuMessenger = QtWidgets.QMenu(self.menuBar)
        self.menuMessenger.setObjectName("menuMessenger")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        Messenger.setMenuBar(self.menuBar)
        self.actionShortcuts = QtWidgets.QAction(Messenger)
        self.actionShortcuts.setObjectName("actionShortcuts")
        self.actionCommands = QtWidgets.QAction(Messenger)
        self.actionCommands.setObjectName("actionCommands")
        self.actionAbout = QtWidgets.QAction(Messenger)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAccount = QtWidgets.QAction(Messenger)
        self.actionAccount.setObjectName("actionAccount")
        self.actionClose = QtWidgets.QAction(Messenger)
        self.actionClose.setObjectName("actionClose")
        self.actionLogout = QtWidgets.QAction(Messenger)
        self.actionLogout.setObjectName("actionLogout")
        self.actionContacts = QtWidgets.QAction(Messenger)
        self.actionContacts.setStatusTip("")
        self.actionContacts.setObjectName("actionContacts")
        self.actionPreferences = QtWidgets.QAction(Messenger)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuMessenger.addAction(self.actionAccount)
        self.menuMessenger.addAction(self.actionPreferences)
        self.menuMessenger.addSeparator()
        self.menuMessenger.addAction(self.actionLogout)
        self.menuMessenger.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionShortcuts)
        self.menuHelp.addAction(self.actionCommands)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionContacts)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuMessenger.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Messenger)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Messenger)

    def retranslateUi(self, Messenger):
        _translate = QtCore.QCoreApplication.translate
        Messenger.setWindowTitle(_translate("Messenger", "Messenger"))
        self.loginLine1.setPlaceholderText(_translate("Messenger", "Login"))
        self.passwordLine1.setPlaceholderText(_translate("Messenger", "Password"))
        self.loginButton.setStatusTip(_translate("Messenger", "Log in to your account"))
        self.loginButton.setText(_translate("Messenger", "Log in"))
        self.loginError1.setText(_translate("Messenger", "<html><head/><body><p><br/></p></body></html>"))
        self.passwordError1.setText(_translate("Messenger", "<html><head/><body><p><br/></p></body></html>"))
        self.signUpLabel.setStatusTip(_translate("Messenger", "Go to registration form"))
        self.signUpLabel.setText(_translate("Messenger", "<html><head/><body><p><span style=\" text-decoration: underline;\">Sign up</span></p></body></html>"))
        self.loginLine2.setPlaceholderText(_translate("Messenger", "Enter Your Login"))
        self.signUpButton.setStatusTip(_translate("Messenger", "Create new account"))
        self.signUpButton.setText(_translate("Messenger", "Sign Up"))
        self.passwordLine2.setPlaceholderText(_translate("Messenger", "Enter Your Password"))
        self.loginLabel.setStatusTip(_translate("Messenger", "Go to login form"))
        self.loginLabel.setText(_translate("Messenger", "<html><head/><body><p><span style=\" text-decoration: underline;\">I am already a member</span></p></body></html>"))
        self.loginError2.setText(_translate("Messenger", "<html><head/><body><p><br/></p></body></html>"))
        self.passwordError2.setText(_translate("Messenger", "<html><head/><body><p><br/></p></body></html>"))
        self.sendButton.setText(_translate("Messenger", "Send"))
        self.messengerLabel.setText(_translate("Messenger", "Python Messenger"))
        self.menuMessenger.setTitle(_translate("Messenger", "Messenger"))
        self.menuHelp.setTitle(_translate("Messenger", "Help"))
        self.actionShortcuts.setText(_translate("Messenger", "Shortcuts"))
        self.actionShortcuts.setStatusTip(_translate("Messenger", "Show available shortcuts"))
        self.actionShortcuts.setShortcut(_translate("Messenger", "Ctrl+S"))
        self.actionCommands.setText(_translate("Messenger", "Commands"))
        self.actionCommands.setStatusTip(_translate("Messenger", "Show available commands"))
        self.actionCommands.setShortcut(_translate("Messenger", "Ctrl+D"))
        self.actionAbout.setText(_translate("Messenger", "About"))
        self.actionAbout.setStatusTip(_translate("Messenger", "Show messenger information"))
        self.actionAccount.setText(_translate("Messenger", "Account"))
        self.actionAccount.setStatusTip(_translate("Messenger", "Open account settings"))
        self.actionAccount.setShortcut(_translate("Messenger", "Ctrl+A"))
        self.actionClose.setText(_translate("Messenger", "Exit"))
        self.actionClose.setStatusTip(_translate("Messenger", "Quit messenger"))
        self.actionLogout.setText(_translate("Messenger", "Logout"))
        self.actionLogout.setStatusTip(_translate("Messenger", "Logout from account"))
        self.actionContacts.setText(_translate("Messenger", "Contacts"))
        self.actionPreferences.setText(_translate("Messenger", "Preferences"))
        self.actionPreferences.setStatusTip(_translate("Messenger", "Edit messenger settings"))
        self.actionPreferences.setShortcut(_translate("Messenger", "Ctrl+R"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Messenger = QtWidgets.QMainWindow()
    ui = Ui_Messenger()
    ui.setupUi(Messenger)
    Messenger.show()
    sys.exit(app.exec_())
