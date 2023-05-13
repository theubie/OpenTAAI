# show_nickname.py
from helpers import write_to_file


def handle_command(line, global_state):
    parts = line.split(" ", 1)
    if len(parts) != 1:
        write_to_file("(From Ai Assistant) Usage: !opentaai show_nickname <twitch_username>", global_state)
        return True

    username = parts[0]
    if not username:
        write_to_file("(From Ai Assistant) Twitch username cannot be empty.", global_state)
        return True

    # Remove the '@' character if present
    username = username.lstrip('@')

    # Look up the nickname in the global state (case-insensitive)
    nickname = global_state.name_changes.get(username.lower())

    if nickname:
        global_state.tts_queue.put(f"{username}'s nickname is '{nickname}'.", global_state)
    else:
        global_state.tts_queue.put(f"{username} does not have a nickname set.", global_state)

    return True


def info():
    return "show_nickname <twitch chat name> - Shows the bot's nickname for a chat user."
