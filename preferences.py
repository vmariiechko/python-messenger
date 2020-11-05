from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from preferences_ui import Ui_Preferences


class PreferencesWindow(QDialog, Ui_Preferences):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        self.server_IP.setText(parent.server_IP)
        self.button_box.button(QDialogButtonBox.Reset).clicked.connect(self.reset)

    def reset(self):
        self.server_IP.setText("127.0.0.1:5000")



