# unpause.py


def handle_command(args, global_state):
    global_state.paused = False
    global_state.tts_queue.put("Resuming chat monitoring operations.  I am now monitoring chat.")


def info():
    return "unpause - Resumes the AI assistant monitoring chat."
