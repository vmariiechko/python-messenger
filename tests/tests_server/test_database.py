import unittest

from sys import path
from os import remove
from sqlite3 import Binary

path.append("../../messenger/server")

from database import *

queries = {
    'create_users_table': """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password_hash BLOB NOT NULL,
                            role INTEGER DEFAULT 1 NOT NULL,
                            registered INTEGER NOT NULL,
                            is_banned INTEGER DEFAULT 0,
                            is_active INTEGER DEFAULT 1 NOT NULL,
                            last_active INTEGER DEFAULT 0 NOT NULL
                            );""",
    'create_messages_table': """CREATE TABLE IF NOT EXISTS messages (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              text TEXT NOT NULL,
                              time INTEGER NOT NULL,
                              user_id INTEGER NOT NULL,
                              FOREIGN KEY (user_id) REFERENCES users (id)
                            );""",
    'add_users': """INSERT INTO
                        users (username, password_hash, registered)
                    VALUES
                        ('Albert', :pwd1, 1604952254),
                        ('Ingrid', :pwd2, 1604953452),
                        ('Dan', :pwd3, 1604954535),
                        ('Susan', :pwd4, 1604955674)""",
    'add_messages':  """INSERT INTO
                            messages (text, time, user_id)
                        VALUES
                            ('Hi there!', 1604953733 , 2),
                            ('Hello', 1604953807 , 1),
                            ('Glad to see you', 1604954018, 3),
                            ('Hi guys', 1604954090, 4),
                            ('What are you doing today?', 1604954152, 2)""",
    'user_message': """SELECT text FROM messages WHERE user_id LIKE :user_id"""
}


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = create_connection('test.sqlite3')
        execute_query(cls.connection, queries['create_users_table'])
        execute_query(cls.connection, queries['create_messages_table'])

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        remove('test.sqlite3')

    def test_create_connection(self):
        self.assertEqual(str(type(self.connection)), "<class 'sqlite3.Connection'>")
        self.assertIsNone(create_connection('./uncorrect/path/to/database.sqlite3'))

    def test_execute_query(self):
        passwords = {'pwd1': Binary(b'alb'), 'pwd2': Binary(b'ing'), 'pwd3': Binary(b'dan'), 'pwd4': Binary(b'sus')}
        self.assertIsNone(execute_query(self.connection, queries['add_users'], passwords))
        self.assertIsNone(execute_query(self.connection, queries['add_messages']))

    def test_execute_read_query(self):
        data = {'user_id': 4}
        user_message = execute_read_query(self.connection, queries['user_message'], 0, data)[0]
        self.assertEqual(user_message, 'Hi guys')


if __name__ == '__main__':
    unittest.main()
