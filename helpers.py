import re


def replace_words_with_pronunciations(text, custom_pronunciations):
    for word, pronunciation in custom_pronunciations.items():
        text = re.sub(re.escape(word), pronunciation, text, flags=re.IGNORECASE)
    return text


def write_to_file(text, global_state):
    file_path = global_state.args.output_file or 'output.txt'
    with open(file_path, 'w') as f:
        f.write(text)

    # And now we also want to direclty write to twitch chat.
    global_state.twitch_queue.put(["send_message", text])


def remove_non_english(text):
    # Regular expression pattern to match non-English characters
    pattern = r'[^a-zA-Z0-9\s]'

    # Remove non-English characters from the text
    processed_text = re.sub(pattern, '', text)

    return processed_text

