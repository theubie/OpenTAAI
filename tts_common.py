import os
import importlib.util
import pyttsx3
from helpers import replace_words_with_pronunciations


def load_tts_apis(global_state):
    global_state.tts_engines = []
    tts_dir = os.path.join(os.path.dirname(__file__), "TTS")
    for file_name in os.listdir(tts_dir):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = file_name[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(tts_dir, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "get_name") and callable(module.get_name):
                global_state.tts_apis.append(module.get_name())


def fallback_tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


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
    tts_dir = os.path.join(os.path.dirname(__file__), "TTS")
    module_name = global_state.tts_engine
    module_path = os.path.join(tts_dir, module_name + ".py")
    if not os.path.exists(module_path):
        print("TTS API module not found. Defaulting to pyttsx3.")
        fallback_tts(text_parsed)
        return

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        # Call the appropriate function within the module
        function_name = "say"
        if hasattr(module, function_name):
            function = getattr(module, function_name)
            function(text_parsed, global_state)
        else:
            print("TTS API module does not have a 'say' function.  Module name is {}".format(global_state.tts_engine))
            fallback_tts(text_parsed)

    except AttributeError:
        print("TTS API module does not have a 'say' function.  Module name is {}".format(global_state.tts_engine))
        fallback_tts(text_parsed)

    except Exception as e:
        print("Error occurred while calling TTS API: {}".format(str(e)))
        fallback_tts(text_parsed)
