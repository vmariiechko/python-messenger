import sys
import unittest

sys.path.append("../../messenger/server")

from server_commands import *


class TestServerCommands(unittest.TestCase):

    def test_get_permissions(self):
        self.assertEqual(get_permissions('Marik'), (3,))
        self.assertEqual(get_permissions('Admin'), (2,))
        self.assertEqual(get_permissions('User'), (1,))
        self.assertIsNone(get_permissions('NotExist'))

    def test_help_client(self):
        self.assertEqual(help_client('Marik'), user_server_commands + moderator_server_commands + admin_server_commands)
        self.assertEqual(help_client('Admin'), user_server_commands + moderator_server_commands)
        self.assertEqual(help_client('User'), user_server_commands)
        self.assertIsNone(help_client('NotExist'))

    def test_myself(self):
        self.assertEqual(myself('Marik'), (1, 3, 1589917631, 1605034299))
        self.assertEqual(myself('Admin'), (29, 2, 1604955062, 1604955075))
        self.assertEqual(myself('User'), (2, 1, 1589917631, 1602174729))
        self.assertIsNone(myself('NotExist'))

    def test_get_online(self):
        self.assertEqual(get_online('Marik'), [])
        self.assertEqual(get_online('NotExist'), [])

    def test_get_registered(self):
        users_count = len(sum(get_registered('Marik'), ()))
        self.assertEqual(users_count, 29)

    def test_ban(self):
        self.assertEqual(ban('Marik', ['Test1', 'Test2', 'Test50'])['result'], 'Not all users exist')
        self.assertEqual(ban('User', ['Test1', 'Test2', 'Test50'])['result'], "You don't have permissions")
        self.assertEqual(ban('NotExist', ['Test1', 'Test2', 'Test50'])['result'], "User doesn't exist")

        self.assertEqual(ban('Marik', ['Test1', 'Test2'])['result'], "Only users were banned<br>")

    def test_unban(self):
        self.assertEqual(unban('Marik', ['Test1', 'Test2', 'Test50'])['result'], 'Not all users exist')
        self.assertEqual(unban('User', ['Test1', 'Test2', 'Test50'])['result'], "You don't have permissions")
        self.assertEqual(unban('NotExist', ['Test1', 'Test2', 'Test50'])['result'], "User doesn't exist")

        self.assertEqual(unban('Marik', ['Test1', 'Test2'])['result'], "Users were unbanned<br>")

    def test_change_role(self):
        self.assertEqual(change_role('NotExist', ['User', '2'])['result'], "User doesn't exist")
        self.assertEqual(change_role('User', ['User', '2'])['result'], "You don't have permissions")
        self.assertEqual(change_role('Marik', ['User', '4'])['result'], "Role isn't specified")
        self.assertEqual(change_role('Marik', ['2'])['result'], "Enter username")
        self.assertEqual(change_role('Marik', ['NotExist', '2'])['result'], "NotExist doesn't exist")
        self.assertEqual(change_role('Marik', ['Marik', '1'])['result'], "It's not allowed to change permissions for "
                                                                         "yourself")
        self.assertEqual(change_role('Marik', ['User', '1'])['result'], "'s permissions was updated successfully<br>")


if __name__ == '__main__':
    unittest.main()
