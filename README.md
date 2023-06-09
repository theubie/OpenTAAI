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

`--chat_file`: The path to the text file containing the chat messages from Twitch. Default is 'chat.txt'.

`--streamer`: The streamer's name (optional).

`--streamer_twitch`: The streamer's Twitch username (optional).

`--streamer_pronouns`: The streamer's pronouns (default: they/them).

`--assistant`: The assistant's name (optional).

`--poll_interval`: The interval to poll the chat file in seconds (default: 5).

`--context`: The context to be used for the OpenAI API request (default: "The bot is an assistant that will read the following stream chat and reply with a summary for the streamer.").

`--context_file`: The path to the text file containing the context to be used for the OpenAI API request (optional, if not provided the script will use the context argument).

`--custom_pronunciations_file`: The path to the JSON file containing custom pronunciations (optional).

`--verbose`: Print out the input text before sending it to OpenAI API (default: false).

`--inactive_chat`: How many seconds to wait for a chat message before the AI tries to engage chat. Set to 0 to disable (default: 30).

`--command_users`: The path to a text file containing user names that are allowed to use the !opentaai command. One user per line (optional).

`--output_file`: The path to a text file to be used by your 3rd party application to send text to the Twitch chat. One message per line. Defaults to "./output.txt".

`--ignored_users_file`: File to store ignored user names in (default: ignored_users.json).

`--attitude`: The current attitude for the bot. Defaults to neutral.

`--timezone`: Timezone you are in. List of timezones can be found at https://pythonhosted.org/pytz/#available-time-zones (default: US/Central).

`--settings`: The path to a json file with settings to load.  If no settings file is specified, settings.txt will be created and updated with the settings at runtime.

`--open_api_key`: The OpenAI API key (optional, if not provided the script will use the api_key_file argument).

`--api_key_file`: The path to the file containing the OpenAI API key (optional, if not provided the script will use the open_api_key argument).

`--model`: The GPT-3 model to use (default: gpt-3.5-turbo).

`--temperature`: The setting for the model's temperature (default: 0.9).

`--llm_api`: Which LLM API to use (default: openai_api).

`--llm_interval`: Number of seconds between calls to the LLM. Defaults to 20.

`--tts_rate`: The speech rate in words per minute (default: 1.0).

`--tts_volume`: The speech volume from 0.0 to 1.0 (default: 1.0).

`--tts_voice`: The speech voice (default: 0).

`--tts_model`: The TTS model to use (default: tts_models/en/ljspeech/tacotron2-DDC_ph).

`--coqui_studio_api_token`: The path to a file containing your Coqui Studio API key (optional).

`--tts_engine`: Which TTS engine to use. Options: coqui, pyttsx3. Defaults to pyttsx3.

`--force_tts_cpu`: Force Coqui TTS to use CPU, even if CUDA is available. Ignore when using pyttsx3. Defaults to False.

`--microphone`: Select the microphone by index or name.

## Example

python main.py --api_key_file api_key.txt --verbose --streamer Ubie --assistant "Stream AI" --context_file context.txt --custom_pronunciations_file custom_words.txt --inactive_chat 0 --coqui_studio_api_token coqui_api_key.txt --streamer_twitch theubie --command_users command_users.txt --tts_engine moegoe --tts_voice 384 --tts_rate 1.3 --llm_api openai_api --microphone "Microphone (NVIDIA Broadcast)" --attitude "snarky and sarcastic" --llm_interval 60

## Future Plans

* Allow using text-generation-webui instead of OpenAI - Mostly Done!
* Allow using other local tts models - In progress.  Coqui, Moegoe, and Pyttsx3 implemented, working on more.
* Integrate a chatbot directly to skip needing a 3rd party to genereate the chat log - Mostly Done!
* Money printer that goes brrr?
