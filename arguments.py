import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Read chat from Twitch channel and get a natural response from OpenAI')
    parser.add_argument('--chat_file', type=str, default='chat.txt',
                        help='Path to the text file containing the chat from Twitch channel')
    parser.add_argument('--open_api_key', type=str, required=False,
                        help='OpenAI API key.  Required if api_key_file is not provided.')
    parser.add_argument('--api_key_file', type=str, required=False,
                        help='Path to the file containing the OpenAI API key. If specified, it will override the '
                             '--api_key argument.')
    parser.add_argument('--streamer', type=str, required=False,
                        help="Streamer's name")
    parser.add_argument('--streamer_twitch', type=str, required=False,
                        help="Streamer's Twitch username")
    parser.add_argument('--assistant', type=str, required=False,
                        help="Assistant's name")
    parser.add_argument('--poll_interval', type=int, default=5,
                        help='Interval to poll the chat file in seconds')
    parser.add_argument('--context', type=str,
                        default="The bot is an assistant that will read the following stream chat "
                                "and reply with a summary for the streamer.",
                        help='The context to be used for the OpenAI API request')
    parser.add_argument('--context_file', type=str, default=None,
                        help='Path to the text file containing the context to be used for the OpenAI API request. If '
                             'specified, it will override the --context argument.')
    parser.add_argument('--custom_pronunciations_file', type=str, default=None,
                        help='Path to the json file containing custom pronunciations')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='Print out the input text before sending it to OpenAI API')
    parser.add_argument('--pyttsx3_rate', type=int, default=200,
                        help='Speech rate in WPM')
    parser.add_argument('--pyttsx3_volume', type=float, default=1.0,
                        help='Speech volume from 0.0 to 1.0')
    parser.add_argument('--pyttsx3_voice', type=int, default=0,
                        help='Speech voice')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo',
                        help='The GPT-3 model to use')
    parser.add_argument('--temperature', type=int, default=0.9,
                        help='Setting for the model\'s temperature')
    parser.add_argument('--poll_quiet_chat', type=int, default=20,
                        help='How many polling attempts before having the assistant talk without chat.  0 to disable.')
    parser.add_argument('--tts_model', type=str, default='tts_models/en/ljspeech/tacotron2-DDC_ph',
                        help='The tts model to use')
    parser.add_argument('--coqui_studio_api_token', type=str, required=False,
                        help='Path to a file containing your Coqui Studio API key.')
    parser.add_argument('--command_users', type=str, required=False, help='Path to a text file containing user names '
                                                                          'that are allowed to use the !opentaai '
                                                                          'command.  One user per line.')
    parser.add_argument('--output_file', type=str, default="output.txt",
                        help='Path to a text file to be used by your 3rd '
                             'party application to send text to the Twitch'
                             ' chat.  One message per line.  Defaults to "./output.txt"')

    parser.add_argument('--tts_engine', type=str, default='pyttsx3', help="Which TTS engine to use.  Options: coqui, "
                                                                          "pyttsx3.  Defaults to pyttsx3")
    parser.add_argument('--force_tts_cpu', type=bool, default=False, help="Force coqui TTS to use CPU even if Cuda is "
                                                                          "available.  Ignore when using pyttsx3.  "
                                                                          "Defaults to False.")
    parser.add_argument('--ignored_users_file', type=str, default='ignored_users.json', help="File to store ignored "
                                                                                             "user names in.")
    parser.add_argument('--attitude', type=str, default='neutral', help="The current attitude for the bot.  Defaults to"
                                                                        " neutral.")
    parser.add_argument('--llm_api', type=str, default='openai_api', help="Which LLM api to use.")
    args = parser.parse_args()
    return args
