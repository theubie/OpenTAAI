# coqui.py
from TTS.api import TTS
import simpleaudio as sa
import torch


def say(text, global_state):
    if global_state.tts_engine_object is None or not isinstance(global_state.tts_engine_object, TTS):
        global_state.tts_engine_object = TTS(model_name=global_state.args.tts_model, progress_bar=False,
                                             gpu=(not global_state.args.force_tts_cpu and torch.cuda.is_available()))

    global_state.tts_engine_object.tts_to_file(text=text, file_path='temp.wav')
    wave_obj = sa.WaveObject.from_wave_file('temp.wav')
    play_obj = wave_obj.play()
    # Wait for playback to finish before exiting
    play_obj.wait_done()
