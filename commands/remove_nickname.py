# remove_nickname.py

import tts_common
from response_commands import save_name_changes
from helpers import write_to_file


def handle_command(line, global_state):
    parts = line.split(" ", 1)
    if len(parts) < 1:
        write_to_file("(From Ai Assistant) Usage: !opentaai remove_nickname <twitch_username>", global_state)
        return True

    username = parts[0]
    if not username:
        write_to_file("(From Ai Assistant) Twitch username cannot be empty.", global_state)
        return True

    # Remove the user's nickname from the global state
    if username in global_state.name_changes:
        del global_state.name_changes[username]
        print(f"Nickname for {username} removed.")
        tts_common.say_something(f"Nickname for {username} removed.", global_state)
        save_name_changes(global_state)
    else:
        print(f"No nickname found for {username}.")

    return True


def info():
    return "remove_nickname <twitch chat name> - Removes a user's nickname."
