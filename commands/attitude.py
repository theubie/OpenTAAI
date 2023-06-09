# attitude.py
from helpers import write_to_file


def handle_command(line, global_state):
    attitude = line.strip()
    if not attitude:
        write_to_file("(From Ai Assistant) Usage: !opentaai attitude <attitude>", global_state)
        return True

    global_state.attitude = attitude
    global_state.tts_queue.put(f"Attitude set to '{attitude}'.", global_state)
    return True


def info():
    return "attitude <attitude> - Sets the bot's attitude."
