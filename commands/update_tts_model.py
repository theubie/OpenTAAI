# update_tts_model.py
from helpers import write_to_file


def handle_command(line, global_state):
    model = line.strip()
    if not model:
        write_to_file("(From Ai Assistant) Usage: !opentaai attitude <attitude>", global_state)
        return True

    global_state.tts_queue.put(["tts_model", model])
    return True


def info():
    return "attitude <attitude> - Sets the bot's attitude."
