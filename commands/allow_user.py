# allow_user.py
import tts_common


def handle_command(args, global_state):
    # args should hold the username that needs to be added.
    if not args:
        print("Please provide a username to add.")
        return

    username = args.strip().lstrip('@')
    if username in global_state.allowed_users:
        print(f"{username} is already in the allowed users list.")
        tts_common.say_something(f"{username} is already on the the allowed users list.", global_state)
    else:
        global_state.allowed_users.add(username)
        print(f"{username} has been added to the allowed users list.")
        tts_common.say_something(f"{username} has been added to the allowed users list.", global_state)

        # Save to file if we need to.
        if global_state.args.command_users:
            try:
                with open(global_state.args.command_users, 'w') as f:
                    f.write("\n".join(global_state.allowed_users))
            except Exception as e:
                print(f"Error writing to command users file: {e}")


def info():
    return "allow_user <username> - Adds the username to the allowed users list for OpenTAAI commands."
