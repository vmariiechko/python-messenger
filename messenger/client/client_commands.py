from datetime import datetime


def help_client(client_commands, server_commands, arg):
    """
    Generates help content.

    If no arg specified, generates main help content,
    otherwise generates help content for specified command.

    :param client_commands: list of dicts with available client-side commands
    :param server_commands: list of dicts with available server-side commands
    :param arg: specified command, optional
    :return: HTML help text
    """

    all_commands = client_commands + server_commands

    # Generate help content only for specified command.
    if len(arg) == 1 and arg[0] in [cmd['name'] for cmd in all_commands]:
        command_desc = [cmd['detailed'] for cmd in all_commands if arg[0] == cmd['name']]

        output = '=' * 40 + '<br>'
        output += command_desc[0] + '<br>'
        output += '=' * 40 + '<br>'

        return output

    # Generate help content for all commands.
    elif not arg:
        output = '=' * 40 + '<br>'
        output += "<b>Enter '/help *command*' to print detailed<br>description of specific command</b><br><br>"
        output += "<span style=\"font-size: 14px\"><table>" \
                  "<tr>" \
                  "<th>Commands&nbsp;&nbsp;</th>" \
                  "<th>Description</th>" \
                  "</tr>"

        for cmd in client_commands:
            output += f"<tr>" \
                      f"<td><code>{cmd['name']}</code></td>" \
                      f"<td>{cmd['description']}</td>" \
                      f"</tr>"

        for cmd in server_commands:
            output += f"<tr>" \
                      f"<td><code>{cmd['name']}</code></td>" \
                      f"<td>{cmd['description']}</td>" \
                      f"</tr>"

        output += "</table></span>"
        output += '=' * 40 + '<br>'
        return output

    else:
        return "<b>Error:</b> Invalid argument. It must be only one available command from '/help' list<br>"


def online(users, args):
    """
    Generates content about online users.

    If no args specified, generates content about all online users,
    otherwise generates content about specified users.

    :param users: list of lists with data about existing users
    :param args: list of all defined usernames, optional
    :return: HTML content about online users
    """

    reg_usernames = [user[0] for user in users]
    users_info = ''
    output = ''

    # Generate content for specified users.
    if args:
        args = list(dict.fromkeys(args))

        # Find unregistered users.
        if len(args) > len(users):
            unregistered = [user for user in args if user not in reg_usernames]
            not_exist = ', '.join(unregistered)

            # More than one user doesn't exist.
            if len(unregistered) > 1:
                output = f"<b>Error:</b> They aren't registered:<br>" \
                         f"{not_exist}<br>" \
                         f"You can type '/reg' to see registered users<br><br>"

            # Only one user doesn't exist.
            else:
                output = f"<b>Error:</b> {not_exist} isn't registered<br>" \
                         f"You can type '/reg' to see registered users<br><br>"

        # Generate content for registered users.
        for user in users:
            if user[1] == 1:
                users_info += f"<b>{user[0]}</b> is online<br>"

            else:
                beauty_time = datetime.fromtimestamp(user[2])
                beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
                users_info += f"<b>{user[0]}</b> was online at {beauty_time}<br>"

        # Combine all generated content above.
        if users_info:
            return output + users_info
        else:
            return output[:-1]

    # Generate content for all online users.
    else:
        online_count = len(reg_usernames)

        # Someone is online except executer.
        if online_count > 1:
            users_info = ', '.join(reg_usernames)
            return f"There are currently {online_count} users online:<br>" \
                   f"<b>{users_info}</b><br>"

        # Only executer is online.
        else:
            return "<b>Nobody is online now apart of you</b><br>"


def status(status, args):
    """
    Generates server status content.

    :param status: dict of server data
    :param args: not used, optional
    :return:  HTML server content
    """

    return f"############ <b>Server Status</b> ###########<br>" \
           f"Server date&time: {status['time']}<br>" \
           f"Registered users: {status['users_count']}<br>" \
           f"Written messages: {status['messages_count']}<br>" \
           f"Users online: {status['users_online']}<br>" + \
           "#" * 34 + "<br>"


def myself(myself, args):
    """
    Generates information about user.

    :param myself: dict of data about user
    :param args: not used, optional
    :return: HTML user information
    """

    myself[2] = datetime.fromtimestamp(myself[2]).strftime('%Y/%m/%d %H:%M:%S')

    if myself[3] == 0:
        myself[3] = 'first entry'
    else:
        myself[3] = datetime.fromtimestamp(myself[3]).strftime('%Y/%m/%d %H:%M:%S')

    # Define what's name of role.
    if myself[1] == 3:
        myself[1] = "Administrator"
    elif myself[1] == 2:
        myself[1] = "Moderator"
    else:
        myself[1] = "User"

    return f"########### <b>Your information</b> ##########<br>" \
           f"ID: {myself[0]}<br>" \
           f"Role: {myself[1]}<br>" \
           f"Registration date&time: {myself[2]}<br>" \
           f"Previous activity: {myself[3]}<br>" + \
           "#" * 34 + "<br>"


def reg(all_usernames, args):
    """
    Generates content about registered users.

    :param all_usernames: list of one-element lists with all registered usernames
    :param args: not used, optional
    :return: HTML content about registered users
    """

    # Concatenate all registered usernames.
    all_usernames = sum(all_usernames, [])
    all_usernames = ', '.join([user for user in all_usernames])
    return f"<b>Registered users:</b> {all_usernames}<br>"


def role(updated, args):
    """
    Generates success message about role changing.

    :param updated: message string about updated permissions
    :param args: username string whom permissions was changed
    :return: HTML message
    """

    return "<b>Success:</b> " + args[0] + updated


def ban(banned, args):
    """
    Generates success message about user blocking.

    :param banned: message string about locking
    :param args: not used, optional
    :return: HTML message
    """

    return "<b>Success:</b> " + banned


def unban(unbanned, args):
    """
    Generates success message about user unblocking.

    :param unbanned: message string about unlocking
    :param args: not used, optional
    :return: HTML message
    """

    return "<b>Success:</b> " + unbanned
