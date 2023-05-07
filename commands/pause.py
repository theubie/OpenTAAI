# pause.py
from tts_common import say_something


def handle_command(args, global_state):
    global_state.paused = True
    say_something("Pausing chat monitoring operations.  I am no longer monitoring chat.", global_state)


def info():
    return "pause - Pauses the AI assistant from monitoring chat."
