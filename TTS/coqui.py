# coqui.py
from TTS.api import TTS
import simpleaudio as sa
import torch
import os
import soundfile as sf
import re


def split_string(text, max_length):
    if len(text) <= max_length:
        return [text]

    # Split the text into sentences
    sentences = re.split(r'(?<=[.?!])\s+', text)

    # Build substrings by concatenating sentences until the length exceeds max_length
    substrings = []
    current_substring = ''
    for sentence in sentences:
        if len(current_substring) + len(sentence) <= max_length:
            current_substring += sentence
        else:
            substrings.append(current_substring.strip())
            current_substring = sentence

    # Append the last substring
    if current_substring:
        substrings.append(current_substring.strip())

    return substrings


def say(text, global_state, event):
    if len(text) > 250:
        substrings = split_string(text, 250)
    else:
        substrings = [text]

    audio_files = []

    for i, substring in enumerate(substrings):
        if global_state.tts_engine_object is None or not isinstance(global_state.tts_engine_object, TTS):
            global_state.tts_engine_object = TTS(model_name=global_state.args.tts_model, progress_bar=False,
                                                 gpu=(
                                                         not global_state.args.force_tts_cpu and torch.cuda.is_available()))
            if global_state.args.verbose:
                print(global_state.tts_engine_object.list_models())
        if substring.strip():
            output_file = f"temp_{i}.wav"
            global_state.tts_engine_object.tts_to_file(text=substring, file_path=output_file, emotion="Neutral")
            audio_files.append(output_file)

    combined_output_file = "combined_output.wav"

    # Concatenate the audio files
    combined_audio = []
    for audio_file in audio_files:
        data, samplerate = sf.read(audio_file, dtype="float32")
        combined_audio.extend(data)

    # Write the combined audio to a new file
    sf.write(combined_output_file, combined_audio, samplerate)

    # Play the combined audio
    wave_obj = sa.WaveObject.from_wave_file(combined_output_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # Clean up the temporary audio files
    for audio_file in audio_files:
        os.remove(audio_file)

    # Clean up the combined output file
    os.remove(combined_output_file)

    event.set()


def update_model(model_name, global_state):
    coqui_model_name = f"coqui_studio/en/OpenTAAI-{model_name}/coqui_studio"

    # Check if coqui_model_name exists in the list of models
    if coqui_model_name not in global_state.tts_engine_object.list_models():
        print(f"Model '{coqui_model_name}' does not exist.")
        return

    global_state.tts_engine_object.load_tts_model_by_name(coqui_model_name,
                                                          not global_state.args.force_tts_cpu and torch.cuda.is_available())
    global_state.args.tts_model = coqui_model_name

    if global_state.args.verbose:
        print(f"Set coqui model to: {model_name} ({coqui_model_name})")

    global_state.tts_queue.put(f"TTS model updated to {model_name}.")
    return
