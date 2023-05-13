# quiet_chat.py
from helpers import write_to_file


def handle_command(args_str, global_state):
    # Check if the argument is a valid integer
    try:
        quiet_chat = int(args_str)
    except ValueError:
        write_to_file("(From Ai Assistant) - Error: argument must be a valid integer.", global_state)
        return True

    # Set the global state variable
    global_state.args.inactive_chat = quiet_chat

    # Output a confirmation message
    write_to_file(f"(From Ai Assistant) - Quiet chat timeout set to {quiet_chat} seconds.", global_state)

    return True
