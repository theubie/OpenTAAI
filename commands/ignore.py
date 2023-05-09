# ignore.py

import tts_common
from helpers import write_to_file
import json


def handle_command(line, global_state):
    parts = line.split(" ", 1)
    if len(parts) != 1:
        write_to_file("(From Ai Assistant) Usage: !opentaai ignore <twitch_username>", global_state)
        print(f"Command had wrong number of arguments.  {parts}")
        return True

    username = parts[0].strip().lower()

    if username in global_state.ignored_users:
        global_state.ignored_users.remove(username)
        write_to_file(f"(From Ai Assistant) Removed {username} from the ignored users list.", global_state)
        print(f"Removed {username} from the ignored users list.")
    else:
        global_state.ignored_users.append(username)
        write_to_file(f"(From Ai Assistant) Added {username} to the ignored users list.", global_state)
        print(f"Added {username} to the ignored users list.")

    # Save the change
    if not global_state.args.ignored_users_file or not global_state.args.ignored_users_file.strip():
        ignored_users_file = "ignored_users.json"
    else:
        ignored_users_file = global_state.args.ignored_users_file

    with open(ignored_users_file, 'w') as f:
        json.dump(global_state.ignored_users, f)

    return True


def info():
    return "ignore <twitch chat name> - Ignores a user's chat messages."
