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
        self.button_box = QtWidgets.QDialogButtonBox(Preferences)
        self.button_box.setGeometry(QtCore.QRect(30, 140, 271, 32))
        self.button_box.setStatusTip("")
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.server_IP = QtWidgets.QLineEdit(Preferences)
        self.server_IP.setGeometry(QtCore.QRect(50, 80, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.server_IP.setFont(font)
        self.server_IP.setToolTip("")
        self.server_IP.setAlignment(QtCore.Qt.AlignCenter)
        self.server_IP.setObjectName("server_IP")
        self.label = QtWidgets.QLabel(Preferences)
        self.label.setGeometry(QtCore.QRect(60, 20, 211, 51))
        self.label.setObjectName("label")

        self.retranslateUi(Preferences)
        self.button_box.accepted.connect(Preferences.accept)
        self.button_box.rejected.connect(Preferences.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "Preferences"))
        self.server_IP.setInputMask(_translate("Preferences", "999.999.999.999:9999"))
        self.server_IP.setText(_translate("Preferences", "1...:"))
        self.label.setText(_translate("Preferences", "<html><head/><body><p><span style=\" font-style:italic; color:#ffffff;\">Don\'t change server IP adress, <br/>if you don\'t know what you\'re doing<br/>Otherwise, you can reset changes</span></p><p><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Preferences = QtWidgets.QDialog()
    ui = Ui_Preferences()
    ui.setupUi(Preferences)
    Preferences.show()
    sys.exit(app.exec_())
