import threading

from database import *


def messages_overflow():
    """ Keeps last 300 messages """
    connection = create_connection("data.sqlite3")
    delete_old = "DELETE from messages WHERE id not in " \
                 "(SELECT id FROM messages ORDER BY time DESC LIMIT 300)"
    execute_query(connection, delete_old)
    connection.close()

    threading.Timer(600, messages_overflow).start()


messages_overflow()
