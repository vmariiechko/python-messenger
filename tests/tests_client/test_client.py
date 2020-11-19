import sys
import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

sys.path.append("../../messenger/client")

from messenger import Messenger


class TestClient(unittest.TestCase):

    def setUp(self):
        self.messenger = Messenger()
        self.login_error = '<span style=" font-style:italic; color:#ffffff;">Login is required</span>'
        self.password_error = '<span style=" font-style:italic; color:#ffffff;">Password is required</span>'

    def test_defaults(self):
        self.assertEqual(self.messenger.login_line1.text(), '')
        self.assertEqual(self.messenger.login_line2.text(), '')

        self.assertEqual(self.messenger.password_line1.text(), '')
        self.assertEqual(self.messenger.password_line2.text(), '')

        self.assertEqual(self.messenger.login_error1.text(), '')
        self.assertEqual(self.messenger.login_error2.text(), '')

        self.assertEqual(self.messenger.password_error1.text(), '')
        self.assertEqual(self.messenger.password_error2.text(), '')

        self.assertEqual(self.messenger.plain_text_edit.toPlainText(), '')

        self.assertIsNone(self.messenger.username)
        self.assertIsNone(self.messenger.password)
        self.assertEqual(self.messenger.last_message_time, 0)
        self.assertEqual(self.messenger.server_IP, '127.0.0.1:5000')

    def test_login(self):
        login = self.messenger.login_button
        QTest.mouseClick(login, Qt.LeftButton)

        self.assertEqual(self.messenger.login_error1.text(), self.login_error)
        self.assertEqual(self.messenger.password_error1.text(), self.password_error)

        self.messenger.login_line1.setText('Marik')
        self.messenger.password_line1.setText('marik')
        QTest.mouseClick(login, Qt.LeftButton)

        self.messenger.plain_text_edit.setPlainText("Hi")
        QTest.mouseClick(self.messenger.send_button, Qt.LeftButton)

    def test_sign_up(self):
        sign_up = self.messenger.sign_up_button
        QTest.mouseClick(sign_up, Qt.LeftButton)

        self.assertEqual(self.messenger.login_error2.text(), self.login_error)
        self.assertEqual(self.messenger.password_error2.text(), self.password_error)

        self.messenger.login_line2.setText('Eagle')
        self.messenger.password_line2.setText('eagle')
        QTest.mouseClick(sign_up, Qt.LeftButton)

        self.messenger.plain_text_edit.setPlainText("krhh")
        QTest.mouseClick(self.messenger.send_button, Qt.LeftButton)


if __name__ == '__main__':
    unittest.main()
