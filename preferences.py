from PyQt5.QtWidgets import QDialog

from preferences_ui import Ui_Preferences


class PreferencesWindow(QDialog, Ui_Preferences):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)


