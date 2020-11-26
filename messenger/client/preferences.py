from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from preferences_ui import Ui_Preferences


class Preferences(QDialog, Ui_Preferences):
    """
    The preferences object contains settings for user.
    """

    def __init__(self, parent=None):
        """Initialize preferences object."""

        super().__init__()
        self.setupUi(self)

        self.server_IP.setText(parent.server_IP)
        self.button_box.button(QDialogButtonBox.Reset).clicked.connect(self.reset)

    def reset(self):
        """Sets server IP address to default value."""

        self.server_IP.setText("0.0.0.0:9000")
