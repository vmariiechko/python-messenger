from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from preferences_ui import Ui_Preferences


class PreferencesWindow(QDialog, Ui_Preferences):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        self.serverIP.setText(parent.server_IP)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.reset)

    def reset(self):
        self.serverIP.setText("127.0.0.1:5000")



