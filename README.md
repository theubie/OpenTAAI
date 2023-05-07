# OpenAI Chatbot

This script is a chatbot that uses OpenAI's GPT-3 API to generate natural responses. It reads a text file containing chat messages from a Twitch channel, and generates a summary for the streamer.

## Requirements

Yes.  There are requirements.  I'll add them here when I have a list.  Obviously you'll need python installed.  If you're on Linux, good luck.  Audio doesn't work on WSL and I don't have an easy way to test yet.  Post in issues and we'll try to figure it all out.
## How to install

* Clone the repo
* Run install.bat or install.sh
* Setup a third party app to capture chat to a text file.  (e.g. Streamdeck, TouchPortal, etc)
* Edit run.bat or run.sh to point to your chat log file and to supply your OpenAI key
* Launch run.bat or run.sh

## How to Use

The script is run with the following parameters:

* `--chat_file`: The path to the text file containing the chat messages from Twitch.

* `--open_api_key`: The OpenAI API key (optional, if not provided the script will use the api_key_file argument).

* `--api_key_file`: The path to the file containing the OpenAI API key (optional, if not provided the script will use the open_api_key argument).

* `--streamer`: The streamer's name (optional).

* `--streamer_twitch`: The streamer's Twitch username (optional).

* `--assistant`: The assistant's name (optional).

* `--poll_interval`: The interval to poll the chat file in seconds (default: 5).

* `--context`: The context to be used for the OpenAI API request (default: "The bot is an assistant that will read the following stream chat and reply with a summary for the streamer.").

* `--context_file`: The path to the text file containing the context to be used for the OpenAI API request (optional, if not provided the script will use the context argument).

* `--custom_pronunciations_file`: The path to the json file containing custom pronunciations (optional).

* `--verbose`: Print out the input text before sending it to OpenAI API (default: false).

* `--rate`: The speech rate (optional).

* `--volume`: The speech volume (optional).

* `--voice`: The speech voice (optional).

* `--model`: The GPT-3 model to use (default: gpt-3.5-turbo).

* `--temperature`: The setting for the model's temperature (default: 0.9).

* `--poll_quiet_chat`: How many polling attempts before having the assistant talk without chat. 0 to disable (default: 20).

* `--tts_model`: The TTS model to use (default: tts_models/en/ljspeech/tacotron2-DDC_ph).

* `--coqui_studio_api_token`: The path to a file containing your Coqui Studio API key (optional).

* `--command_users`: The path to a text file containing user names that are allowed to use the !opentaai command. One user per line (optional).

* `--output_file`: The path to a text file to be used by your 3rd party application to send text to the Twitch chat. One message per line. Defaults to "./output.txt".

* `--tts_engine`: Which TTS engine to use. Options: coqui, pyttsx3. Defaults to pyttsx3.

* `--tts_force_cpu`: Force coqui tts to use cpu, even if cuda is available.

## Example

python openai-chatbot.py --chat_file d:/stream/chat.txt --api_key_file d:/stream/openai_api_key.txt --streamer StreamerName --assistant AssistantName --context_file d:/stream/context.txt --custom_pronunciations_file d:/stream/custom_pronunciations.json --verbose --rate 100 --volume 10 --voice 5

## Future Plans

* Allow using text-generation-webui instead of OpenAI
* Allow using other local tts models - In progress.  Coqui and Pyttsx3 implemented, working on more.
* Integrate a chatbot directly to skip needing a 3rd party to genereate the chat log
* Money printer that goes brrr?
