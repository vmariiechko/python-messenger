import sys
import unittest

sys.path.append("../../messenger/server")

from database import *

queries = {
    'add_messages':  """INSERT INTO
                            messages (text, time, user_id)
                        VALUES
                            ('Hi there!', 1604954152, 2),
                            ('Hello', 1604954090, 1),
                            ('Glad to see you', 1604954018, 3),
                            ('Hi guys', 1604953807, 4),
                            ('What are you doing today?', 1604953733, 2)""",
    'user_message': """SELECT text FROM messages WHERE user_id LIKE :user_id"""
}


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = create_connection('data.sqlite3')

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_create_connection(self):
        self.assertEqual(str(type(self.connection)), "<class 'sqlite3.Connection'>")
        self.assertEqual(create_connection('./uncorrect/path/database.sqlite3'), None)

    def test_execute_query(self):
        self.assertIsNone(execute_query(self.connection, queries['add_messages']))

    def test_execute_read_query(self):
        data = {'user_id': 4}
        user_message = execute_read_query(self.connection, queries['user_message'], 0, data)[0]
        self.assertEqual(user_message, 'Hi guys')


if __name__ == '__main__':
    unittest.main()
