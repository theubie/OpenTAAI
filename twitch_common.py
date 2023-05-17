# twitch_common.py
import time
import twitchio
from twitchio.ext import commands, pubsub


class Bot(commands.Bot):
    _global_state = None

    def __init__(self, global_state):
        self._global_state = global_state
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=self._global_state.twitch_token, prefix='?',
                         initial_channels=[global_state.args.streamer_twitch])

    async def sub_main(self):
        topics = [
            pubsub.channel_points(self._global_state.twitch_token)[self.user_id],
            pubsub.bits(self._global_state.twitch_token)[self.user_id]
        ]
        await self.client.pubsub.subscribe_topics(topics)
        await self.client.start()

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        print(f'Connected channels | {self.connected_channels}')
        self.loop.create_task(self.get_current_game())

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        if self._global_state.verbose:
            print(f"Twitch Thread: message: {message.author.display_name}: {message.content}")

        # put the message into the queue to process.
        self._global_state.main_queue.put(f"{message.author.display_name}: {message.content}")

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

    def send_chat_message(self, message):
        # Limit the message to 500 characters
        message = message[:500]
        chan = self.get_channel(self._global_state.args.streamer_twitch)
        self.loop.create_task(chan.send(f"From OpenTAAI: {message}"))

    def send_chat_whisper(self, user, message):
        # Split the message into parts if it exceeds 500 characters
        message_parts = [message[i:i + 400] for i in range(0, len(message), 400)]

        # chan = self.get_channel(self._global_state.args.streamer_twitch)
        if self._global_state.args.verbose:
            print(f"Trying to get channel for {user}")
        chan = self.get_channel(user)
        for part in message_parts:
            self.loop.create_task(chan.whisper(part))
            time.sleep(0.5)

    async def get_current_game(self):
        channels = await self.fetch_channels([self.user_id])
        if len(channels) > 0:
            self._global_state.current_game = channels[0].game_name
