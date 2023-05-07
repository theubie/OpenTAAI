# remove_user.py
import tts_common


def handle_command(args, global_state):
    # args should hold the username that needs to be removed.
    if not args:
        print("Please provide a username to remove.")
        return

    username = args.strip().lstrip('@')
    if username not in global_state.allowed_users:
        print(f"{username} is not in the allowed users list.")
        tts_common.say_something(f"{username} is not on the allowed users list.", global_state)
    else:
        if global_state.args.streamer_twitch and username == global_state.args.streamer_twitch:
            print(f"{username} cannot be removed from the allowed users list.")
            tts_common.say_something(f"{username} is the streamer and cannot be removed from the allowed users list.",
                                     global_state)
        else:
            global_state.allowed_users.remove(username)
            print(f"{username} has been removed from the allowed users list.")
            tts_common.say_something(f"{username} has been removed from the allowed users list.", global_state)
            # Save to file if we need to.
            if global_state.args.command_users:
                with open(global_state.args.command_users, 'w') as f:
                    f.write("\n".join(global_state.allowed_users))


def info():
    return "remove_user <username> - Removes the username from the allowed users list for OpenTAAI commands.  Note:  " \
           "The streamer can not be removed from this list."
