# reset_history.py
import os


def info():
    return "Clears the chat history for the bot."


def handle_command(args, global_state):
    # Set the shutdown_requested flag to initiate a graceful shutdown
    if global_state.context_file and os.path.isfile(global_state.context_file):
        with open(global_state.context_file, "r") as context_file_handle:
            context = context_file_handle.read()
    if global_state.args.streamer:
        context += " The streamer's name is " + global_state.args.streamer + ", and the assistant should refer to the streamer as that. "
    if global_state.args.streamer_twitch:
        context += " The streamer's twitch chat username name is " + global_state.args.streamer_twitch + ". "
    if global_state.args.assistant:
        context += " The assistant's name is " + global_state.args.assistant + ", and the assistant should refer to themselves as that. "

    global_state.messages = [{"role": "system", "content": context}]   # Clear and reset content.

    global_state.context = context

    global_state.tts_queue.put("LLM Chat history reset.")
    print("LLM Chat history reset.")