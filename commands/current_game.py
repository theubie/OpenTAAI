# current_game.py

def handle_command(args, global_state):
    global_state.current_game = args.strip()
    global_state.tts_queue.put(f"Current game set to: {global_state.current_game}")
    print(f"Current game set to: {global_state.current_game}")


def info():
    return "Sets the current game being played on stream."
