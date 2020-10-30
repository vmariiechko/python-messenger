# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(332, 178)
        self.buttonBox = QtWidgets.QDialogButtonBox(Preferences)
        self.buttonBox.setGeometry(QtCore.QRect(30, 140, 271, 32))
        self.buttonBox.setStatusTip("")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.serverIP = QtWidgets.QLineEdit(Preferences)
        self.serverIP.setGeometry(QtCore.QRect(50, 80, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.serverIP.setFont(font)
        self.serverIP.setToolTip("")
        self.serverIP.setAlignment(QtCore.Qt.AlignCenter)
        self.serverIP.setObjectName("serverIP")
        self.label = QtWidgets.QLabel(Preferences)
        self.label.setGeometry(QtCore.QRect(60, 20, 211, 51))
        self.label.setObjectName("label")

        self.retranslateUi(Preferences)
        self.buttonBox.accepted.connect(Preferences.accept)
        self.buttonBox.rejected.connect(Preferences.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "Preferences"))
        self.serverIP.setStatusTip(_translate("Preferences", "Enter IP"))
        self.serverIP.setInputMask(_translate("Preferences", "999.999.999.999:9999"))
        self.serverIP.setText(_translate("Preferences", "1...:"))
        self.serverIP.setPlaceholderText(_translate("Preferences", "Enter Server IP"))
        self.label.setText(_translate("Preferences", "<html><head/><body><p><span style=\" font-style:italic; color:#ffffff;\">Don\'t change server IP adress <br/>if you don\'t know what you\'re doing<br/>Otherwise, you can reset changes</span></p><p><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Preferences = QtWidgets.QDialog()
    ui = Ui_Preferences()
    ui.setupUi(Preferences)
    Preferences.show()
    sys.exit(app.exec_())
