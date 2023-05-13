# pause.py

def handle_command(args, global_state):
    global_state.paused = True
    global_state.tts_queue.put("Pausing chat monitoring operations.  I am no longer monitoring chat.", global_state)


def info():
    return "pause - Pauses the AI assistant from monitoring chat."
