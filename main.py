import os
import time
import openai
import json

import globals
import tts_common
import response_commands
from commands import parse_opentaai_command
from globals import GlobalState

# Create a global state instance
from helpers import replace_words_with_pronunciations

# get our arguments

# our global variables
global_state = GlobalState()


def send_to_openai(lines, context):
    input_str = response_commands.replace_names("\n".join(lines))
    global_state.messages.append({"role": "user", "content": input_str})
    total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in global_state.messages)
    while total_tokens > global_state.MAX_TOKENS - global_state.RESPONSE_TOKENS:
        global_state.messages.pop(1)
        total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in global_state.messages)
    input_text = context + "\n" + "\n".join(lines)
    if global_state.verbose:
        print(f"Input text: \n{global_state.messages}")
    openai.api_key = api_key.strip()

    try:
        response = openai.ChatCompletion.create(
            model=global_state.args.model,
            messages=global_state.messages,
            temperature=global_state.args.temperature
        )
    except openai.OpenAIError as e:
        print(f"Error: {e}")
        return "Sorry, an error occurred while processing your request. Please try again later."
    else:
        new_response = response_commands.process_response(response['choices'][0]['message']['content'])
        global_state.messages.append({"role": "assistant", "content": new_response})
        return new_response


if __name__ == "__main__":

    # Setup Coqui API key if it's provided.
    if global_state.args.coqui_studio_api_token:
        try:
            with open(global_state.args.coqui_studio_api_token, 'r') as file:
                api_key = file.read().strip()
                os.environ['COQUI_STUDIO_TOKEN'] = api_key
        except FileNotFoundError:
            print(f"Error: Could not find file '{global_state.args.coqui_studio_api_token}'")
    else:
        print("'coqui-studio-api-token' argument not provided.  Skipping.")

    # do any required setup for our response_commands
    response_commands.module_setup()

    # Check for arguments and assign defaults
    if global_state.args.api_key_file and os.path.isfile(global_state.args.api_key_file):
        with open(global_state.args.api_key_file, "r") as api_key_file_handle:
            api_key = api_key_file_handle.read()

    if global_state.context_file and os.path.isfile(global_state.context_file):
        with open(global_state.context_file, "r") as context_file_handle:
            context = context_file_handle.read()
    if global_state.args.streamer:
        context += " The streamer's name is " + global_state.args.streamer + ", and the assistant should refer to the streamer as that. "
    if global_state.args.assistant:
        context += " The assistant's name is " + global_state.args.assistant + ", and the assistant should refer to themselves as that. "

    # Stuff our context into our messages.
    global_state.messages.append({"role": "system", "content": context})

    if not os.path.isfile(global_state.file_path):
        print(f"File not found: {global_state.file_path}")
        with open(global_state.file_path, mode="w") as f:
            pass  # create an empty file

    # delete the contents of the file
    with open(global_state.file_path, "w") as f:
        f.write("")

    if global_state.custom_pronunciations_file and not os.path.isfile(global_state.custom_pronunciations_file):
        print(f"File not found: {global_state.custom_pronunciations_file}")
        exit()

    # load custom pronunciations
    if global_state.custom_pronunciations_file:
        with open(global_state.custom_pronunciations_file, "r") as custom_file:
            global_state.custom_pronunciations = json.load(custom_file)
    else:
        global_state.custom_pronunciations = None

    startup_message = ["Chat assistant starting."]
    if global_state.args.streamer:
        startup_message.append(f"Setting streamer name to {global_state.args.streamer}.")
    if global_state.args.assistant:
        startup_message.append(f"Setting assistant name to {global_state.args.assistant}.")
    startup_message.append("Configuration complete.  I am now monitoring chat.")
    print("\n".join(startup_message))
    tts_common.say_something("\n".join(startup_message), global_state)

    poll_count = 0
    while True:
        try:
            with open(global_state.file_path, "r") as file:
                lines = file.readlines()
                if lines:
                    # delete the contents of the file
                    with open(global_state.file_path, "w") as f:
                        f.write("")
                    poll_count = 0
                    # remove any blank lines and strip whitespace from remaining lines and strip out commands
                    # but parse any commands for our script.
                    new_lines = []
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        message = line.split(": ")[1]
                        if message.startswith("!opentaai"):
                            if parse_opentaai_command(line, global_state):
                                continue
                        elif message.startswith("!"):
                            continue
                        if message.startswith("(From Ai Assistant)"):
                            continue
                        new_lines.append(line)
                    lines = new_lines

                    # send lines to OpenAI API
                    if not global_state.paused and len(lines) > 0:
                        response = send_to_openai(lines, context)
                        # do something with the response here, like sending it to a TTS engine
                        print(response)

                        if global_state.verbose:
                            print(f"{response}")
                        tts_common.say_something(response, global_state)

                else:
                    if not global_state.paused and global_state.args.poll_quiet_chat > 0:
                        poll_count = poll_count + 1
                        print(f"Number of polls since last chat: {poll_count} (Max: {global_state.args.poll_quiet_chat})")
                        if poll_count >= global_state.args.poll_quiet_chat:
                            poll_count = 0
                            # send lines to OpenAI API
                            response = send_to_openai([
                                "There have been no new chat messages for a while.  Please engage in banter with the "
                                "streamer and chat or say something to help move chat along."],
                                context)
                            # do something with the response here, like sending it to a TTS engine
                            print(response)
                            if global_state.custom_pronunciations:
                                response_parsed = replace_words_with_pronunciations(response,
                                                                                    global_state.custom_pronunciations[
                                                                                        'pronunciations'])
                            else:
                                response_parsed = response

                            if global_state.verbose:
                                print(f"{response_parsed}")
                            tts_common.say_something(response_parsed, global_state)

        except FileNotFoundError:
            print(f"File not found: {global_state.file_path}")
        time.sleep(global_state.delay_seconds)
