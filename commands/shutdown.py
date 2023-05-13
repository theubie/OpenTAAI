# shutdown.py

def info():
    return "Shuts down the chat assistant."


def handle_command(args, global_state):
    # Set the shutdown_requested flag to initiate a graceful shutdown
    global_state.tts_queue.put("Shutdown command received.  Shutting down.")
    print("Shutdown command received.  Initiating shutdown.")
    global_state.running = False
