import re


def replace_words_with_pronunciations(text, custom_pronunciations):
    for word, pronunciation in custom_pronunciations.items():
        text = re.sub(re.escape(word), pronunciation, text, flags=re.IGNORECASE)
    return text


def write_to_file(text, global_state):
    file_path = global_state.args.output_file or 'output.txt'
    with open(file_path, 'w') as f:
        f.write(text)

