import os
import time
import openai
import re
import argparse
import pyttsx3
import json

parser = argparse.ArgumentParser(description='Read chat from Twitch channel and get a natural response from OpenAI')
parser.add_argument('--chat_file', type=str, default='d:/stream/chat.txt',
                    help='Path to the text file containing the chat from Twitch channel')
parser.add_argument('--open_api_key', type=str, required=False,
                    help='OpenAI API key.  Required if api_key_file is not provided.')
parser.add_argument('--api_key_file', type=str, required=False,
                    help='Path to the file containing the OpenAI API key. If specified, it will override the '
                         '--api_key argument.')
parser.add_argument('--streamer', type=str, required=False,
                    help="Streamer's name")
parser.add_argument('--assistant', type=str, required=False,
                    help="Assistant's name")
parser.add_argument('--poll_interval', type=int, default=5,
                    help='Interval to poll the chat file in seconds')
parser.add_argument('--context', type=str, default="The bot is an assistant that will read the following stream chat "
                                                   "and reply with a summary for the streamer.",
                    help='The context to be used for the OpenAI API request')
parser.add_argument('--context_file', type=str, default=None,
                    help='Path to the text file containing the context to be used for the OpenAI API request. If '
                         'specified, it will override the --context argument.')
parser.add_argument('--custom_pronunciations_file', type=str, default=None,
                    help='Path to the json file containing custom pronunciations')
parser.add_argument('--verbose', action='store_true', default=False,
                    help='Print out the input text before sending it to OpenAI API')
parser.add_argument('--rate', type=int, default=None,
                    help='Speech rate')
parser.add_argument('--volume', type=int, default=None,
                    help='Speech volume')
parser.add_argument('--voice', type=int, default=None,
                    help='Speech voice')
parser.add_argument('--model', type=str, default='gpt-3.5-turbo',
                    help='The GPT-3 model to use')
parser.add_argument('--temperature', type=int, default=0.9,
                    help='Setting for the model\'s temperature')
args = parser.parse_args()

# Check for arguments and assign defaults
file_path = args.chat_file
api_key = args.open_api_key
if args.api_key_file and os.path.isfile(args.api_key_file):
    with open(args.api_key_file, "r") as api_key_file_handle:
        api_key = api_key_file_handle.read()
delay_seconds = args.poll_interval
context = args.context
context_file = args.context_file
if context_file and os.path.isfile(context_file):
    with open(context_file, "r") as context_file_handle:
        context = context_file_handle.read()
if args.streamer:
    context += " The streamer's name is " + args.streamer + ", and the assistant should refer to the streamer as that. "
if args.assistant:
    context += " The assistant's name is " + args.assistant + ", and the assistant should refer to themselves as that. "

messages = [
    {"role": "system", "content": context},
]
custom_pronunciations_file = args.custom_pronunciations_file
verbose = args.verbose

if not os.path.isfile(file_path):
    print(f"File not found: {file_path}")
    with open(file_path, mode="w") as f:
        pass  # create an empty file
if custom_pronunciations_file and not os.path.isfile(custom_pronunciations_file):
    print(f"File not found: {custom_pronunciations_file}")
    exit()

MAX_TOKENS = 2048  # change this to the max token limit you want to set
RESPONSE_TOKENS = 150  # change this to the number of tokens you want to make available for the response


def send_to_openai(lines, context):
    global messages
    messages.append({"role": "user", "content": "\n".join(lines)})
    total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in messages)
    while total_tokens > MAX_TOKENS - RESPONSE_TOKENS:
        messages.pop(1)
        total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in messages)
    input_text = context + "\n" + "\n".join(lines)
    if verbose:
        print(f"Input text: \n{messages}")
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature
        )
    except openai.OpenAIError as e:
        print(f"Error: {e}")
        return "Sorry, an error occurred while processing your request. Please try again later."
    else:
        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        return response['choices'][0]['message']['content']


engine = pyttsx3.init()
# Custom settings
if args.rate:
    engine.setProperty('rate', args.rate)
if args.volume:
    engine.setProperty('volume', args.volume)
if args.voice:
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[args.voice].id if args.voice < len(voices) else voices[0].id)

# load custom pronunciations
if custom_pronunciations_file:
    with open(custom_pronunciations_file, "r") as custom_file:
        custom_pronunciations = json.load(custom_file)
        engine.setProperty('voice', custom_pronunciations['pronunciations'])
else:
    custom_pronunciations = None


def replace_words_with_pronunciations(text, custom_pronunciations):
    for word, pronunciation in custom_pronunciations.items():
        text = re.sub(re.escape(word), pronunciation, text, flags=re.IGNORECASE)
    return text


while True:
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if lines:
                # remove any blank lines and strip whitespace from remaining lines
                lines = [line.strip() for line in lines if line.strip()]
                # send lines to OpenAI API
                response = send_to_openai(lines, context)
                # do something with the response here, like sending it to a TTS engine
                print(response)
                if custom_pronunciations:
                    response_parsed = replace_words_with_pronunciations(response,
                                                                        custom_pronunciations['pronunciations'])
                else:
                    response_parsed = response

                if args.verbose:
                    print(f"{response_parsed}")
                engine.say(response_parsed)
                engine.runAndWait()
                # delete the contents of the file
                with open(file_path, "w") as f:
                    f.write("")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    time.sleep(delay_seconds)
