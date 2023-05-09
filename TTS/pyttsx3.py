# pyttsx3.py
import pyttsx3


def say(text, global_state):
    if global_state.tts_engine_object is None or not isinstance(global_state.tts_engine_object, pyttsx3.engine.Engine):
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

    global_state.tts_engine_object.say(text)
    global_state.tts_engine_object.runAndWait()
