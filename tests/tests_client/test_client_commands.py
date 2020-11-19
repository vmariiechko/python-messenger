import sys
import unittest

sys.path.append("../../messenger/client")

from client_commands import *


class TestClientCommands(unittest.TestCase):

    def test_status(self):
        info = {'time': 1605125906, 'users_count': 20, 'messages_count': 200, 'users_online': 2}
        self.assertIs(type(status(info, "Anything")), str)

    def test_myself(self):
        info = [5, 2, 1589917741, 1605125906]
        self.assertIs(type(myself(info, "Anything")), str)

    def test_reg(self):
        usernames = [['User'], ['Admin'], ['John'], ['Daniel']]
        self.assertEqual(reg(usernames, 'Anything'), "<b>Registered users:</b> User, Admin, John, Daniel<br>")

    def test_role(self):
        self.assertEqual(role("'s permissions was updated successfully<br>", ['Admin']), "<b>Success:</b> Admin's "
                                                                                         "permissions was updated "
                                                                                "successfully<br>")

    def test_ban(self):
        self.assertEqual(ban('Only users were banned<br>', 'User'), '<b>Success:</b> Only users were banned<br>')
        self.assertEqual(unban('Only users were banned<br>', 'User'), '<b>Success:</b> Only users were banned<br>')


if __name__ == '__main__':
    unittest.main()
