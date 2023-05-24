from arguments import parse_args
import json
import os
import datetime
import pytz
from queue import Queue


class GlobalState:
    def __init__(self):
        self.paused = False
        self.running = True
        self.args = parse_args()
        self.messages = []
        self.custom_pronunciations = None
        self.context = self.args.context
        self.file_path = self.args.chat_file
        self.api_key = self.args.open_api_key
        self.delay_seconds = self.args.poll_interval
        self.context_file = self.args.context_file
        self.custom_pronunciations_file = self.args.custom_pronunciations_file
        self.verbose = self.args.verbose
        self.MAX_TOKENS = 2048
        self.RESPONSE_TOKENS = 150
        self.name_changes = {}
        self.ignored_users = []
        self.attitude = self.args.attitude
        self.llm_apis = []
        self.llm_api = self.args.llm_api
        self.tts_engines = []
        self.tts_engine = self.args.tts_engine
        self.tts_engine_object = None
        self.current_game = None
        self.context = ""
        self.twitch_token = ""
        self.twitch_user_id = 29601546
        RETRY_DELAY_SECONDS = 5
        MAX_RETRIES = 3


        # Queues
        self.main_queue = Queue()
        self.tts_queue = Queue()
        self.llm_queue = Queue()
        self.twitch_queue = Queue()

        self.allowed_users = set()

        # Set allowed_users based on command line arguments
        self.allowed_users.add("VOICE COMMAND")

        if parse_args().streamer_twitch:
            self.allowed_users.add(parse_args().streamer_twitch.strip())

        if parse_args().command_users:
            try:
                with open(parse_args().command_users, 'r') as f:
                    for line in f:
                        self.allowed_users.add(line.strip())
            except FileNotFoundError:
                print(
                    f"Warning: command_users file {parse_args().command_users} not found.")

        if not self.allowed_users:
            raise ValueError("At least one user must be allowed to execute commands.  Either specify the user's "
                             "twitch username with --streamer_twitch <username> or create a text file with allowed "
                             "users, one user name per line, and specify its path with --command_users <path>.")

        try:
            if not self.args.ignored_users_file or not self.args.ignored_users_file.strip():
                ignored_users_file = "ignored_users.json"
            else:
                ignored_users_file = self.args.ignored_users_file

            with open(ignored_users_file, 'r') as f:
                try:
                    self.ignored_users = json.load(f)
                except:
                    self.ignored_user = []

        except FileNotFoundError:
            pass

        # API Key for LLM
        if self.args.api_key_file and os.path.isfile(self.args.api_key_file):
            with open(self.args.api_key_file, "r") as api_key_file_handle:
                self.api_key = api_key_file_handle.read()

        # API Key for coqui studio
        if self.args.coqui_studio_api_token and os.path.isfile(self.args.coqui_studio_api_token):
            with open(self.args.coqui_studio_api_token, "r") as api_key_file_handle:
                coqui_api = api_key_file_handle.read().strip()
                os.environ["COQUI_STUDIO_TOKEN"] = coqui_api

        # Twitch Token
        if self.args.twitch_token_file and os.path.isfile(self.args.twitch_token_file):
            with open(self.args.twitch_token_file, "r") as twitch_token_handle:
                self.twitch_token = twitch_token_handle.read()

    def relevant_string(self):
        # Set the timezone
        timezone = pytz.timezone(self.args.timezone)

        # Get the current time in the timezone
        current_time = datetime.datetime.now(timezone)

        # Format the time
        formatted_time = current_time.strftime("%A %B %d %Y, %I:%M%p")
        relevant_info = f"It is currently {formatted_time}"

        if self.current_game is not None:
            relevant_info = relevant_info + f" Currently we are playing/streaming: {self.current_game}"

        return relevant_info
