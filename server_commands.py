from database import *

select_queries = {
    'select_all_usernames': """SELECT username FROM users""",
    'select_active_users': """SELECT username FROM users WHERE is_active = 1"""
}

user_server_commands = [
    {'name': 'help', 'description': 'Prints available commands',
     'detailed': '#Usage: /help <command>\n\n'
                 'Prints available commands if no argument.\n'
                 'Prints detailed description of <command> If argument <command> is specified.\n\n'
                 '#Examples:\n'
                 '/help  ->  prints all available commands\n'
                 '/help reg  ->  prints detailed info about \'/reg\''},
    {'name': 'myself', 'description': 'Prints info about you',
     'detailed': '#Usage: /myself\n'
                 'Prints next information about you:\n'
                 'ID, role, registration date, last activity.'},
    {'name': 'status', 'description': 'Prints server status',
     'detailed': '#Usage: /status\n'
                 'Prints next information about server:\n'
                 'Server time, registered users count, written messages count.'},
    {'name': 'online', 'description': 'Prints online users',
     'detailed': '#Usage: /online <usernames>\n\n'
                 'Prints online users if there are no argument.\n'
                 'If <usernames> specified, prints users status.\n\n'
                 '#Examples:\n'
                 '/online  ->  prints all online users\n'
                 '/online User1 User2  ->  prints User1 & User2 status'},
    {'name': 'reg', 'description': 'Prints registered users',
     'detailed': '#Usage: /reg\n'
                 'Prints usernames of all registered users.'},
]

moderator_server_commands = [
    {'name': 'ban', 'description': 'Ban users',
     'detailed': '#Usage: /ban <usernames>\n\n'
                 'Ban specified <usernames>\n\n'
                 '#Example:\n'
                 '/ban User1 User2 -> ban User1 and User2'},
    {'name': 'unban', 'description': 'Unban users',
     'detailed': '#Usage: /unban <usernames>\n\n'
                 'Unban specified <usernames>\n\n'
                 '#Example:\n'
                 '/unban User1 User2 -> unban User1 and User2,'},
]

admin_server_commands = [
    {'name': 'role', 'description': 'Change role of user',
     'detailed': "#Usage: /role <username> <role>\n\n"
                 "Change user permissions.\n"
                 "Argument <role> can be '1', '2' or '3'\n"
                 "Where 1-user, 2-moderator, 3-administrator\n\n"
                 "#Example:\n"
                 "/role Bob 2  ->  change Bob's role to 'moderator'"},
]


def checkPermissions(username):
    connection = createConnection("data.sqlite3")

    select_permission = f"SELECT role " \
                        f"FROM users " \
                        f"WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_permission, 0, {'username': username})

    connection.close()
    return query_data


def helpClient(username):
    role = checkPermissions(username)

    if role[0] == 1:
        return user_server_commands
    elif role[0] == 2:
        return user_server_commands + moderator_server_commands
    elif role[0] == 3:
        return user_server_commands + moderator_server_commands + admin_server_commands


def myself(username, *args):
    connection = createConnection("data.sqlite3")

    select_user = f"SELECT id, role, registered, last_active " \
                  f"FROM users " \
                  f"WHERE username LIKE :username"
    query_data = executeReadQuery(connection, select_user, 0, {'username': username})

    connection.close()
    return query_data


def online(username, args=None):
    connection = createConnection("data.sqlite3")

    if args:
        select_users = f"SELECT username, is_active, last_active " \
                       f"FROM users " \
                       f"WHERE username IN ({','.join(['?'] * len(args))})"
        query_data = executeReadQuery(connection, select_users, 1, args)

    else:
        query_data = executeReadQuery(connection, select_queries['select_active_users'])

    connection.close()
    return query_data


def reg(*args):
    connection = createConnection("data.sqlite3")

    all_usernames = select_queries['select_all_usernames']
    query_data = executeReadQuery(connection, all_usernames)

    connection.close()
    return query_data


def ban(username, args, flag=1):
    all_usernames = reg()
    all_usernames = sum(all_usernames, ())

    if not all(username in all_usernames for username in args):
        return {'ok': False, 'result': 'Not all users exist'}

    connection = createConnection("data.sqlite3")

    if flag:
        ban_users = f"UPDATE users " \
                    f"SET is_banned = 1 " \
                    f"WHERE username IN ({','.join(['?'] * len(args))})" \
                    f"AND role = 1"
        executeQuery(connection, ban_users, args)
        result = 'Only users were banned\n'

    else:
        unban_users = f"UPDATE users " \
                      f"SET is_banned = 0 " \
                      f"WHERE username IN ({','.join(['?'] * len(args))})"
        executeQuery(connection, unban_users, args)
        result = 'Users were unbanned\n'

    connection.close()
    return {'ok': True, 'result': result}


def unban(username, args):
    return ban(username, args, 0)


def role(username, args):
    permission = args[-1]

    if permission not in ('1', '2', '3'):
        return {'ok': False, 'result': "Role isn't specified"}
    elif len(args) != 2:
        return {'ok': False, 'result': "Enter username"}
    elif username is None:
        return {'ok': False, 'result': "Can't detect your username"}

    all_usernames = reg()
    user = args[0]

    if user not in [usernames[0] for usernames in all_usernames]:
        return {'ok': False, 'result': f"{user} doesn't exist"}

    if user == username:
        return {'ok': False, 'result': "It's not allowed to change permissions for yourself"}

    connection = createConnection("data.sqlite3")

    data_dict = {'permission': permission, 'username': user}
    update_role = f"UPDATE users " \
                  f"SET role = :permission " \
                  f"WHERE username LIKE :username"
    executeQuery(connection, update_role, data_dict)

    connection.close()
    return {'ok': True, 'result': '\'s permissions was updated successfully\n'}
