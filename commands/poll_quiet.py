# poll_quiet.py
from helpers import write_to_file


def handle_command(args_str, global_state):
    # Check if the argument is a valid integer
    try:
        poll_quiet_chat = int(args_str)
    except ValueError:
        write_to_file("(From Ai Assistant) - Error: argument must be a valid integer.", global_state)
        return True

    # Set the global state variable
    global_state.args.poll_quiet_chat = poll_quiet_chat

    # Output a confirmation message
    write_to_file(f"(From Ai Assistant) - Quiet chat polling set to {poll_quiet_chat} intervals.", global_state)

    return True
