from datetime import datetime


def helpClient(client_commands, server_commands, args):
    all_commands = client_commands + server_commands

    if len(args) == 1 and args[0] in [cmd['name'] for cmd in all_commands]:
        detailed_info = [cmd['detailed'] for cmd in all_commands if args[0] == cmd['name']]

        output = '=' * 41 + '<br>'
        output += detailed_info[0] + '<br>'
        output += '=' * 41 + '<br>'

        return output

    elif not args:
        output = '=' * 41 + '<br>'
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
        output += '=' * 41 + '<br>'
        return output

    else:
        return "<b>Error:</b> Invalid argument. It must be only one available command from '/help' list<br>"


def online(users, args):
    reg_usernames = [user[0] for user in users]
    users_info = ''
    output = ''

    if args:
        args = list(dict.fromkeys(args))

        if len(args) > len(users):
            unregistered = [user for user in args if user not in reg_usernames]
            not_exist = ', '.join(unregistered)

            if len(unregistered) > 1:
                output = f"<b>Error:</b> They aren't registered:<br>" \
                         f"{not_exist}<br>" \
                         f"You can type '/reg' to see registered users<br><br>"

            else:
                output = f"<b>Error:</b> {not_exist} isn't registered<br>" \
                         f"You can type '/reg' to see registered users<br><br>"

        for user in users:
            if user[1] == 1:
                users_info += f"<b>{user[0]}</b> is online<br>"

            else:
                beauty_time = datetime.fromtimestamp(user[2])
                beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
                users_info += f"<b>{user[0]}</b> was online at {beauty_time}<br>"

        if users_info:
            return output + users_info
        else:
            return output[:-1]

    else:
        online_count = len(reg_usernames)

        if online_count > 1:
            users_info = ', '.join(reg_usernames)
            return f"There are currently {online_count} users online:<br>" \
                   f"<b>{users_info}</b><br>"

        else:
            return "<b>Nobody is online now apart of you</b><br>"


def status(status, args):
    return f"############ <b>Server Status</b> ############<br>" \
           f"Server date&time: {status['time']}<br>" \
           f"Registered users: {status['users_count']}<br>" \
           f"Written messages: {status['messages_count']}<br>" + \
           "#" * 34 + "<br>"


def myself(myself, args):
    myself[2] = datetime.fromtimestamp(myself[2]).strftime('%Y/%m/%d %H:%M:%S')
    myself[3] = datetime.fromtimestamp(myself[3]).strftime('%Y/%m/%d %H:%M:%S')

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
    all_usernames = sum(all_usernames, [])
    all_usernames = ', '.join([user for user in all_usernames])
    return f"<b>Registered users:</b> {all_usernames}<br>"


def role(updated, args):
    return "<b>Success:</b> " + args[0] + updated


def ban(banned, args):
    return "<b>Success:</b> " + banned


def unban(unbanned, args):
    return "<b>Success:</b> " + unbanned
