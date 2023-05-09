# set_nickname.py

import tts_common
from response_commands import save_name_changes
from helpers import write_to_file


def handle_command(line, global_state):
    parts = line.split(" ", 2)
    if len(parts) < 2:
        write_to_file("(From Ai Assistant) Usage: !opentaai set_nickname <twitch_username> <nickname>", global_state)
        return True

    username, nickname = parts[0], parts[1]
    if not username:
        write_to_file("(From Ai Assistant) Twitch username cannot be empty.", global_state)
        return True

    # Remove the '@' character if present
    username = username.lstrip('@')

    # Save the nickname in the global state (case-insensitive)
    global_state.name_changes[username.lower()] = nickname.lower()

    print(f"Nickname for {username} set to '{nickname}'.")
    tts_common.say_something(f"Nickname for {username} set to '{nickname}'.", global_state)
    save_name_changes(global_state)

    return True


def info():
    return "set_nickname <twitch chat name> <nickname> - Makes the bot used a different name for a chat user."
