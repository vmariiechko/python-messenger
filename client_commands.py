from datetime import datetime


def helpClient(client_commands, server_commands, args):
    all_commands = client_commands + server_commands

    if len(args) == 1 and args[0] in [cmd['name'] for cmd in all_commands]:
        detailed_info = [cmd['detailed'] for cmd in all_commands if args[0] == cmd['name']]

        output = '=' * 41 + '\n'
        output += detailed_info[0] + '\n'
        output += '=' * 41 + '\n'

        return output

    elif not args:
        output = '=' * 41 + '\n'
        output += f"#Enter '/help <command>' to print detailed description of specific command\n\n" \
                  f"{'Command':<15}Description\n"

        for cmd in client_commands:
            output += '{name:<17}{description:<}'.format(**cmd) + '\n'

        for cmd in server_commands:
            output += '{name:<17}{description:<}'.format(**cmd) + '\n'

        output += '=' * 41 + '\n'
        return output

    else:
        return "Error: Invalid argument. It must be only one available command from '/help' list\n"


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
                output = f"Error: They aren't registered:\n" \
                         f"{not_exist}\n" \
                         f"You can type '/reg' to see registered users\n\n"

            else:
                output = f"Error: {not_exist} isn't registered\n" \
                         f"You can type '/reg' to see registered users\n\n"

        for user in users:
            if user[1] == 1:
                users_info += f"{user[0]} is online\n"

            else:
                beauty_time = datetime.fromtimestamp(user[2])
                beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M:%S')
                users_info += f"{user[0]} was online at {beauty_time}\n"

        if users_info:
            return output + users_info
        else:
            return output[:-1]

    else:
        online_count = len(reg_usernames)

        if online_count > 1:
            users_info = ', '.join(reg_usernames)
            return f"There are currently {online_count} users online:\n" \
                   f"{users_info}\n"

        else:
            return "Nobody is online now apart of you\n"


def status(status, args):
    return f"############ Server Status ############\n" \
           f"Server date&time: {status['time']}\n" \
           f"Registered users: {status['users_count']}\n" \
           f"Written messages: {status['messages_count']}\n" + \
           "#" * 34 + "\n"


def myself(myself, args):
    myself[2] = datetime.fromtimestamp(myself[2]).strftime('%Y/%m/%d %H:%M:%S')
    myself[3] = datetime.fromtimestamp(myself[3]).strftime('%Y/%m/%d %H:%M:%S')

    if myself[1] == 3:
        myself[1] = "Administrator"
    elif myself[1] == 2:
        myself[1] = "Moderator"
    else:
        myself[1] = "User"

    return f"########### Your information ###########\n" \
           f"ID: {myself[0]}\n" \
           f"Role: {myself[1]}\n" \
           f"Registration date&time: {myself[2]}\n" \
           f"Previous activity: {myself[3]}\n" + \
           "#" * 34 + "\n"


def reg(all_usernames, args):
    all_usernames = sum(all_usernames, [])
    all_usernames = ', '.join([user for user in all_usernames])
    return f"Registered users: {all_usernames}\n"


def role(updated, args):
    return "Success: " + args[0] + updated


def ban(banned, args):
    return "Success: " + banned


def unban(unbanned, args):
    return "Success: " + unbanned
