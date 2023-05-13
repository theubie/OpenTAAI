# pyttsx3.py
import pyttsx3
import time


def say(text, global_state, event):
    if global_state.tts_engine_object is None or not isinstance(global_state.tts_engine_object, pyttsx3.engine.Engine):
        if global_state.args.verbose:
            print("Creating pyttsx3 engine.")
        global_state.tts_engine_object = pyttsx3.init()

    # set our voice, rate, and volume
    voices = global_state.tts_engine_object.getProperty('voices')
    if global_state.args.pyttsx3_voice < len(voices):
        voice = voices[global_state.args.pyttsx3_voice]
    else:
        # default to the first voice
        voice = voices[0]
        print(f"Invalid voice index, defaulting to {voice.name}")
    global_state.tts_engine_object.setProperty('voice', voice.id)
    global_state.tts_engine_object.setProperty('rate', global_state.args.pyttsx3_rate)
    global_state.tts_engine_object.setProperty('volume', global_state.args.pyttsx3_volume)

    # if the engine is busy, wait.
    # if global_state.args.verbose:
    #     print(f"Checking if engine is busy. {global_state.tts_engine_object.isBusy()}")
    # while global_state.tts_engine_object.isBusy():
    #     time.sleep(0.1)
    #
    global_state.tts_engine_object.say(text)
    global_state.tts_engine_object.runAndWait()
    event.set()

