# unpause.py
from tts_common import say_something


def handle_command(args, global_state):
    global_state.paused = False
    say_something("Resuming chat monitoring operations.  I am now monitoring chat.", global_state)


def info():
    return "unpause - Resumes the AI assistant monitoring chat."
