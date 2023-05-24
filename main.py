import os
import time
import json
from queue import Queue
from queue import Empty

import tts_common
import llm_common
import twitch_common
import response_commands
from commands import parse_opentaai_command
from globals import GlobalState
# from stt_common import stt_thread, enumerate_microphones
import asyncio
import twitch_subpub

# Global variables
global_state = GlobalState()


async def main_loop(global_state):
    print("Main Thread: Started.")

    # load our name changes
    response_commands.load_name_changes(global_state)

    # Handle Chat file at startup.

    if not os.path.isfile(global_state.file_path):
        print(f"File not found: {global_state.file_path}")
        with open(global_state.file_path, mode="w"):
            pass  # Create an empty file

    with open(global_state.file_path, "w"):
        pass  # Delete the contents of the file

    # Initial context setup.
    startup_message = ["Open T A AI Bot Startup."]
    if global_state.context_file and os.path.isfile(global_state.context_file):
        with open(global_state.context_file, "r") as context_file_handle:
            context = context_file_handle.read()
    if global_state.args.streamer:
        context += f" The streamer's name is {global_state.args.streamer}, and the assistant should refer to the streamer as that. "
        startup_message.append(f"Setting Streamer name to {global_state.args.streamer}.")

    # This isn't political...the AI literally doesn't know who you are.
    if global_state.args.streamer_pronouns:
        context += f" The streamer's pronouns are {global_state.args.streamer_pronouns}."

    if global_state.args.streamer_twitch:
        context += f" The streamer's twitch chat username name is {global_state.args.streamer_twitch}. "

    if global_state.args.assistant:
        context += f" The assistant's name is {global_state.args.assistant}, and the assistant should refer to themselves as that. "
        startup_message.append(f"Setting Assistant name to {global_state.args.assistant}.")

    startup_message.append("Open T A AI Bot Now monitoring chat.")
    global_state.tts_queue.put("\n".join(startup_message))

    global_state.messages = [{"role": "system", "content": context}]  # Clear and reset content.

    global_state.context = context

    poll_count = time.time()

    while global_state.running:

        try:
            with open(global_state.file_path, "r+", encoding="utf-8") as file:
                lines = file.readlines()

                # check our queue
                try:
                    while True:
                        item = global_state.main_queue.get_nowait()
                        if lines:
                            lines.append(item)
                        else:
                            lines = [item]
                except Empty:
                    pass

                if lines:
                    # delete the contents of the file
                    file.seek(0)
                    file.truncate()
                    # Remove blank lines, strip whitespace from remaining lines, and strip out commands
                    # while parsing any commands for our script.
                    new_lines = []
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        username = line.split(": ")[0]
                        message = line.split(": ")[1]
                        if message.startswith("!opentaai"):
                            if parse_opentaai_command(line, global_state):
                                continue
                        elif message.startswith("!"):
                            continue
                        if message.startswith("(From Ai Assistant)"):
                            continue
                        if username.lower() in global_state.ignored_users:
                            continue
                        new_lines.append(response_commands.process_response(line, global_state))
                    lines = new_lines

                    # Send lines to OpenAI API
                    if not global_state.paused and len(lines) > 0:
                        global_state.llm_queue.put(lines)
                        # Update the last chat message time since we have actual chat messages.
                        poll_count = time.time()

                else:
                    if not global_state.paused and global_state.args.inactive_chat > 0:
                        elapsed_time = time.time() - poll_count
                        if global_state.args.verbose:
                            print(f"Number of seconds since last chat: {elapsed_time} "
                                  f"(Max: {global_state.args.inactive_chat})")
                        if elapsed_time >= global_state.args.inactive_chat:
                            poll_count = time.time()  # Reset the last chat message time
                            global_state.llm_queue.put([
                                "There have been no new chat messages for a while.  Please engage in banter with the "
                                "streamer and chat or say something to help move chat along."])

        except FileNotFoundError:
            print(f"File not found: {global_state.file_path}")
        await asyncio.sleep(global_state.delay_seconds)
    print("Main Thread: Stopped.")


async def tts_thread(global_state):
    print("TTS Thread: Started.")
    while global_state.running or global_state.tts_queue.qsize() != 0:
        if global_state.tts_queue.qsize() != 0:
            response = global_state.tts_queue.get()
            if isinstance(response, list):
                # response[0] should be what value changed, and response[1] should be the new value.
                if response[0] == "tts_model":
                    tts_common.update_model(response[1], global_state)

            else:
                # Handle string response
                event = asyncio.Event()
                tts_common.say_something(response, global_state, event)
                await event.wait()
        await asyncio.sleep(1)
    print("TTS Thread: Stopped.")


async def llm_thread(global_state):
    print("LLM Thread: Started.")
    queue_items = []  # List to store the items in the queue
    last_sent_time = time.time() - global_state.args.llm_interval  # Initialize the last sent time
    while global_state.running or global_state.llm_queue.qsize() != 0:
        if global_state.llm_queue.qsize() != 0:
            current_time = time.time()
            if current_time - last_sent_time >= global_state.args.llm_interval:
                # Collect all the items in the queue
                while global_state.llm_queue.qsize() != 0:
                    lines = global_state.llm_queue.get()
                    queue_items.extend(lines)

                # Make a single call to llm_common with all the items
                response = llm_common.send_to_llm(queue_items, global_state.context, global_state)
                if global_state.verbose:
                    print(f"{response}")
                global_state.tts_queue.put(response)

                # Reset the queue and last sent time
                queue_items = []
                last_sent_time = current_time
        await asyncio.sleep(1)
    print("LLM Thread: Stopped.")


async def twitch_thread(global_state):
    print("Twitch Thread: Started.")
    bot = twitch_common.Bot(global_state)

    # Run the bot and the stop condition checker concurrently
    try:
        async def check_stop_condition():
            last_game_check = time.time()
            while global_state.running:
                # Check the Twitch queue for messages
                while not global_state.twitch_queue.empty():
                    item = global_state.twitch_queue.get()
                    if item[0] == "send_message":
                        bot.send_chat_message(item[1])
                    elif item[0] == "send_whisper":
                        bot.send_chat_whisper(item[1], item[2])

                # Perform periodic game checks every 10 seconds
                if time.time() - last_game_check >= 10:
                    await bot.get_current_game()
                    last_game_check = time.time()

                await asyncio.sleep(0.5)  # Use a smaller delay for responsiveness

            # Trigger the stop condition if global_state.running is False
            await stop_bot()

        async def stop_bot():
            # Stop the bot
            await bot.close()

        bot_task = asyncio.create_task(bot.start())
        stop_condition_task = asyncio.create_task(check_stop_condition())

        await asyncio.wait([bot_task, stop_condition_task], return_when=asyncio.FIRST_COMPLETED)

        # Cancel any remaining tasks
        for task in [bot_task, stop_condition_task]:
            if not task.done():
                task.cancel()

    except asyncio.CancelledError:
        pass

    print("Twitch Thread: Stopped.")



async def main(global_state):
    tasks = [
        asyncio.create_task(main_loop(global_state)),
        asyncio.create_task(tts_thread(global_state)),
        asyncio.create_task(llm_thread(global_state)),
        asyncio.create_task(twitch_thread(global_state)),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    global_state.running = True

    # Call the enumerate_microphones function to list available microphones
    # enumerate_microphones(global_state)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(global_state))
    finally:
        loop.close()
