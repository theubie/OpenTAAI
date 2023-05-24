import mymoegoe.tts as mytts
import simpleaudio as sa
import time
import sounddevice as sd


def say(text, global_state, event):
    if mytts.n_symbols == 0:
        if global_state.verbose:
            print(f"Loading moegoe model.")

        mytts.loadtts("b")

        if global_state.verbose:
            print(f"Total voices in this model: {len(mytts.hps_ms.speakers)}")
            print(f"Speaker ({global_state.args.tts_voice}) info: {mytts.hps_ms.speakers[global_state.args.tts_voice]}")

    text = text.replace("\n", " ")
    try:
        if global_state.verbose:

            print(f"Sending {text} to moegoe tts")
            start_time = time.time()

        audio = mytts.tts(text, "d:/OpenTAAI/temp.wav", global_state.args.tts_voice, global_state.args.tts_rate, True)
        sd.play(audio, samplerate=mytts.hps_ms.data.sampling_rate, blocking=True)

        if global_state.verbose:
            gen_time = time.time()
            print(f"TTS generated and saved as file in {gen_time - start_time} seconds.")

    except Exception as e:
        print("Failed to generate tts")
        print(f"Error: {e}")
        raise

    # wave_obj = sa.WaveObject.from_wave_file("d:/OpenTAAI/temp.wav")
    # play_obj = wave_obj.play()
    # play_obj.wait_done()
    if global_state.verbose:
        play_time = time.time()
        print(
            f"TTS playback is {play_time - gen_time} seconds.  Total end to end time {play_time - start_time} seconds.")

    event.set()
