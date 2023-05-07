from TTS.api import TTS
import simpleaudio as sa
import pyttsx3
from helpers import replace_words_with_pronunciations
import torch


def say_something(text, global_state):
    if global_state.custom_pronunciations:
        text_parsed = replace_words_with_pronunciations(text,
                                                        global_state.custom_pronunciations['pronunciations'])
    else:
        text_parsed = text

    # Check to see if the bot replied with their name, and if so, axe that.
    if global_state.args.assistant:
        assistant_name = global_state.args.assistant.lower()
    else:
        assistant_name = "assistant"

    if text_parsed.lower().startswith(assistant_name + ":"):
        text_parsed = text_parsed[len(assistant_name) + 1:]

    # Determine which TTS engine to use based on user input
    if not hasattr(global_state.args, 'tts_engine') or global_state.args.tts_engine == 'coqui':
        tts = TTS(model_name=global_state.args.tts_model, progress_bar=False, gpu=(not global_state.args.force_tts_cpu and torch.cuda.is_available()))

        tts.tts_to_file(text=text_parsed, file_path='temp.wav')

        wave_obj = sa.WaveObject.from_wave_file('temp.wav')
        play_obj = wave_obj.play()
        # Wait for playback to finish before exiting
        play_obj.wait_done()

    elif global_state.args.tts_engine == 'pyttsx3':
        engine = pyttsx3.init()
        engine.say(text_parsed)
        engine.runAndWait()

    else:
        print("Invalid TTS engine specified. Defaulting to pyttsx3.")
        engine = pyttsx3.init()
        engine.say(text_parsed)
        engine.runAndWait()

    return
