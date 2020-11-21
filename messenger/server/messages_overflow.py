from threading import Timer

from database import (create_connection, execute_query, execute_read_query)


def messages_overflow():
    """Keeps last 300 messages in database every 10 minutes."""

    connection = create_connection("data.sqlite3")
    delete_old_messages = "DELETE from messages WHERE id not in " \
                          "(SELECT id FROM messages ORDER BY time DESC LIMIT 300)"
    execute_query(connection, delete_old_messages)
    connection.close()

    Timer(600, messages_overflow).start()


messages_overflow()
