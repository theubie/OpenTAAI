# stt_common.pyy
import pyaudio
import time
from helpers import remove_non_english
import re

import speech_recognition as sr


def stt_thread(global_state):
    print("STT Thread: Starting.")

    # Trigger phrases to detect
    trigger_phrases = ["Hey AI", "Hey Assistant", f"Hey {global_state.args.assistant}"]
    command_phrase = "AI command"

    # this is called from the background thread
    def callback(recognizer, audio):
        try:
            text = recognizer.recognize_whisper(audio)
            text = remove_non_english(text)
            text = re.sub(r'\b\s*underscore\s*\b', '_', text, flags=re.IGNORECASE)
            print("Whisper Speech Recognition thinks you said: " + text)

            # Check if the recognized text contains any of the trigger phrases
            for phrase in trigger_phrases:
                if phrase.lower() in text.lower():
                    # Put the recognized text in a list and add it to the LLM queue
                    if global_state.args.streamer_twitch:
                        username = global_state.args.streamer_twitch
                    elif global_state.args.streamer:
                        username = global_state.args.streamer
                    else:
                        username = "streamer"
                    global_state.llm_queue.put([f"{username}: {text}"])
                    return  # Exit the function after processing trigger phrases

            # Check if the recognized text contains the command phrase
            if command_phrase.lower() in text.lower():
                # Process it as a special command
                command = text.lower().replace(command_phrase.lower(), "VOICE COMMAND: !opentaai")
                global_state.main_queue.put(command.strip())
                return  # Exit the function after processing the command phrase

        except sr.UnknownValueError:
            print("Whisper Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Whisper; {0}".format(e))

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.energy_threshold = 4000
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # Listen until we are no longer running.
    while global_state.running:
        time.sleep(0.1)  # wait for us to stop running.

    # calling this function requests that the background listener stop listening
    stop_listening(wait_for_stop=False)
    print("STT Thread: Stopped.")


def enumerate_microphones(global_state):
    selected_microphone = global_state.args.microphone
    audio = pyaudio.PyAudio()

    # Get the number of available devices
    device_count = audio.get_device_count()

    print("Available Microphones:")
    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        device_name = device_info['name']
        if global_state.args.verbose:
            print(f"STT Thread: Device {i + 1}: {device_name}")

        if selected_microphone and (selected_microphone.isdigit() and int(
                selected_microphone) == i + 1 or selected_microphone.lower() in device_name.lower()):
            # Match found for the selected microphone
            print(f"STT Thread: Selected Microphone: {device_name}")
            global_state.args.microphone = device_name
            break

    audio.terminate()
