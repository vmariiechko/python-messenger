# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'messenger.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Messenger(object):
    def setupUi(self, Messenger):
        Messenger.setObjectName("Messenger")
        Messenger.resize(410, 610)
        self.centralwidget = QtWidgets.QWidget(Messenger)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 410, 581))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.loginLine1 = QtWidgets.QLineEdit(self.page)
        self.loginLine1.setGeometry(QtCore.QRect(60, 160, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loginLine1.setFont(font)
        self.loginLine1.setText("")
        self.loginLine1.setObjectName("loginLine1")
        self.passwordLine1 = QtWidgets.QLineEdit(self.page)
        self.passwordLine1.setGeometry(QtCore.QRect(60, 220, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passwordLine1.setFont(font)
        self.passwordLine1.setObjectName("passwordLine1")
        self.loginButton1 = QtWidgets.QPushButton(self.page)
        self.loginButton1.setGeometry(QtCore.QRect(120, 290, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.loginButton1.setFont(font)
        self.loginButton1.setObjectName("loginButton1")
        self.messengerLabel1 = QtWidgets.QLabel(self.page)
        self.messengerLabel1.setGeometry(QtCore.QRect(70, 30, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.messengerLabel1.setFont(font)
        self.messengerLabel1.setObjectName("messengerLabel1")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.page_2)
        self.textBrowser.setGeometry(QtCore.QRect(20, 100, 371, 401))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.sendButton = QtWidgets.QPushButton(self.page_2)
        self.sendButton.setGeometry(QtCore.QRect(320, 530, 71, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sendButton.setFont(font)
        self.sendButton.setObjectName("sendButton")
        self.messengerLabel2 = QtWidgets.QLabel(self.page_2)
        self.messengerLabel2.setGeometry(QtCore.QRect(70, 30, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.messengerLabel2.setFont(font)
        self.messengerLabel2.setObjectName("messengerLabel2")
        self.textEdit = QtWidgets.QTextEdit(self.page_2)
        self.textEdit.setGeometry(QtCore.QRect(20, 520, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.stackedWidget.addWidget(self.page_2)
        Messenger.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Messenger)
        self.statusbar.setObjectName("statusbar")
        Messenger.setStatusBar(self.statusbar)

        self.retranslateUi(Messenger)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Messenger)

    def retranslateUi(self, Messenger):
        _translate = QtCore.QCoreApplication.translate
        Messenger.setWindowTitle(_translate("Messenger", "Messenger"))
        self.loginLine1.setPlaceholderText(_translate("Messenger", "Login"))
        self.passwordLine1.setPlaceholderText(_translate("Messenger", "Password"))
        self.loginButton1.setText(_translate("Messenger", "Log in"))
        self.messengerLabel1.setText(_translate("Messenger", "Python Messenger"))
        self.sendButton.setText(_translate("Messenger", "Send"))
        self.messengerLabel2.setText(_translate("Messenger", "Python Messenger"))
