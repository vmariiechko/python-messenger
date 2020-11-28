from database import (create_connection, execute_query, execute_read_query)

select_queries = {
    'select_all_usernames': """SELECT username FROM users""",
    'select_active_users': """SELECT username FROM users WHERE is_active = 1"""
}

user_server_commands = [
    {'name': 'help', 'description': 'Prints available commands',
     'detailed': "<b>Usage:</b> /help *command*<br><br>"
                 "Prints available commands if no argument.<br>"
                 "Prints detailed description of *command* If argument *command* is specified.<br><br>"
                 "<b>Examples:</b><br>"
                 "/help  ->  prints all available commands<br>"
                 "/help reg  ->  prints detailed info about '/reg'"},
    {'name': 'myself', 'description': 'Prints info about you',
     'detailed': '<b>Usage:</b> /myself<br><br>'
                 'Prints next information about you:<br>'
                 'ID, role, registration date, last activity.'},
    {'name': 'status', 'description': 'Prints server status',
     'detailed': '<b>Usage:</b> /status<br><br>'
                 'Prints next information about server:<br>'
                 'Server time, registered users count, written messages count.'},
    {'name': 'online', 'description': 'Prints online users',
     'detailed': "<b>Usage:</b> /online *usernames*<br><br>"
                 "Prints online users if there are no argument.<br>"
                 "If *usernames* specified, prints users' status.<br><br>"
                 "<b>Examples:</b><br>"
                 "/online  ->  prints all online users<br>"
                 "/online User1 User2  ->  prints User1 & User2 status"},
    {'name': 'reg', 'description': 'Prints registered users',
     'detailed': '<b>Usage:</b> /reg<br><br>'
                 'Prints usernames of all registered users.'},
]

moderator_server_commands = [
    {'name': 'ban', 'description': 'Ban users',
     'detailed': '<b>Usage:</b> /ban *usernames*<br><br>'
                 'Ban specified *usernames*<br><br>'
                 '<b>Example:</b><br>'
                 '/ban User1 User2 -> ban User1 and User2'},
    {'name': 'unban', 'description': 'Unban users',
     'detailed': '<b>Usage:</b> /unban *usernames*<br><br>'
                 'Unban specified *usernames*<br><br>'
                 '<b>Example:</b><br>'
                 '/unban User1 User2 -> unban User1 and User2,'},
]

admin_server_commands = [
    {'name': 'role', 'description': 'Change role of user',
     'detailed': "<b>Usage:</b> /role *username* *role*<br><br>"
                 "Change user's permissions.<br>"
                 "Argument *role* can be '1', '2' or '3'<br>"
                 "Where 1-user, 2-moderator, 3-administrator<br><br>"
                 "<b>Example:</b><br>"
                 "/role Bob 2  ->  change Bob's role to 'moderator'"},
]


def get_permissions(username):
    """
    Checks on user's permissions.

    There're 3 numbers for the permissions: 1, 2 and 3.
    Where: 1 - User, 2 - Moderator, 3 - Administrator.

    :param username: who executed the command
    :return: one-element tuple with number for the permissions
    """

    connection = create_connection("data.sqlite3")

    select_permission = f"SELECT role " \
                        f"FROM users " \
                        f"WHERE username LIKE :username"
    query_data = execute_read_query(connection, select_permission, 0, {'username': username})

    connection.close()
    return query_data


def help_client(username):
    """
    Defines available commands depending on the permissions.

    :param username: who executed the command
    :return: list of dicts with available commands due to the permissions
    """

    role = get_permissions(username)

    if not role:
        return None
    elif role[0] == 1:
        return user_server_commands
    elif role[0] == 2:
        return user_server_commands + moderator_server_commands
    elif role[0] == 3:
        return user_server_commands + moderator_server_commands + admin_server_commands


def myself(username, *args):
    """
    Queries user's data.

    Executes read query to get user's data:
        - id
        - permissions
        - date of registration in seconds
        - date of last activity in seconds

    :param username: who executed the command
    :return: tuple of user's data
    """

    connection = create_connection("data.sqlite3")

    select_user = f"SELECT id, role, registered, last_active " \
                  f"FROM users " \
                  f"WHERE username LIKE :username"
    query_data = execute_read_query(connection, select_user, 0, {'username': username})

    connection.close()
    return query_data


def get_online(username, args=None):
    """
    Checks if there're online users.

    With no args parameter searches for all online users.
    With specified args parameter searches only for specified ones.
    User's data tuple contains:
        - username
        - is active (1 - Yes, 0 - No)
        - date of last activity in seconds

    :param username: who executed the command
    :param args: list of usernames, optional
    :return: list of tuples with users' data about their activity
    """

    connection = create_connection("data.sqlite3")

    if args:
        select_users = f"SELECT username, is_active, last_active " \
                       f"FROM users " \
                       f"WHERE username IN ({','.join(['?'] * len(args))})"
        query_data = execute_read_query(connection, select_users, 1, args)

    else:
        query_data = execute_read_query(connection, select_queries['select_active_users'])

    connection.close()
    return query_data


def get_registered(*args):
    """
    Queries all registered users.

    :param args: not used, optional
    :return: list of one-element tuples with registered usernames
    """

    connection = create_connection("data.sqlite3")

    all_usernames = select_queries['select_all_usernames']
    query_data = execute_read_query(connection, all_usernames)

    connection.close()
    return query_data


def ban(username, args, flag=1):
    """
    Blocks user to log in.

    Depending on the flag parameter, this function can block or unblock user.
    Only moderators and administrators can execute this command

    :param username: who executed the command
    :param args: list with usernames to block
    :param flag: switch, 1 - ban user, 0 - unban user
    :return: dict of execution status
    :rtype: {
        'ok': bool
        'result': str
    }
    """

    # Verify executer of permissions.
    role = get_permissions(username)
    if not role:
        return {'ok': False, 'result': "User doesn't exist"}
    elif role[0] not in (2, 3):
        return {'ok': False, 'result': "You don't have permissions"}

    all_usernames = get_registered()
    all_usernames = sum(all_usernames, ())

    # Find unregistered users.
    if not all(username in all_usernames for username in args):
        return {'ok': False, 'result': 'Not all users exist'}

    connection = create_connection("data.sqlite3")

    # Ban user.
    if flag:
        ban_users = f"UPDATE users " \
                    f"SET is_banned = 1 " \
                    f"WHERE username IN ({','.join(['?'] * len(args))})" \
                    f"AND role = 1"
        execute_query(connection, ban_users, args)
        result = 'Only users were banned<br>'

    # Unban user.
    else:
        unban_users = f"UPDATE users " \
                      f"SET is_banned = 0 " \
                      f"WHERE username IN ({','.join(['?'] * len(args))})"
        execute_query(connection, unban_users, args)
        result = 'Users were unbanned<br>'

    connection.close()
    return {'ok': True, 'result': result}


def unban(username, args):
    """Allow (unblock) user to log in. Same as :func:`ban`."""

    return ban(username, args, 0)


def change_role(username, args):
    """
    Changes role for specified user.

    Command takes only 2 arguments:
        - username
        - number of role (1 - User, 2 - Moderator, 3 - Administrator)
    Only administrators can execute this command

    :param username: who executed the command
    :param args: list of two strings: username and number of role
    :return: dict of execution status
    :rtype: {
        'ok': bool
        'result': str
    }
    """

    # Verify executer of permissions.
    role = get_permissions(username)
    if not role:
        return {'ok': False, 'result': "User doesn't exist"}
    elif role[0] not in (2, 3):
        return {'ok': False, 'result': "You don't have permissions"}

    # Verify amount of arguments
    if len(args) != 2:
        return {'ok': False, 'result': "Invalid number of arguments.<br>"
                                       "Type '/help role' to see specification<br>"}

    permission = args[1]

    # Validate command syntax.
    if permission not in ('1', '2', '3'):
        return {'ok': False, 'result': "Role isn't specified"}

    all_usernames = get_registered()
    user = args[0]

    # Find unregistered users.
    if user not in [usernames[0] for usernames in all_usernames]:
        return {'ok': False, 'result': f"{user} doesn't exist"}

    if user == username:
        return {'ok': False, 'result': "It's not allowed to change permissions for yourself"}

    # Change role.
    connection = create_connection("data.sqlite3")

    data_dict = {'permission': permission, 'username': user}
    update_role = f"UPDATE users " \
                  f"SET role = :permission " \
                  f"WHERE username LIKE :username"
    execute_query(connection, update_role, data_dict)

    connection.close()
    return {'ok': True, 'result': "'s permissions was updated successfully<br>"}
