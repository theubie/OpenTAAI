import time
import twitchio
import asyncio
from twitchio.ext import pubsub


async def main(global_state):
    my_token = global_state.twitch_token
    users_oauth_token = global_state.twitch_token
    users_channel_id = global_state.twitch_user_id
    client = twitchio.Client(token=my_token)
    client.pubsub = pubsub.PubSubPool(client)

    print(f"token: {users_oauth_token}  id: {users_channel_id}")
    topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id],
        pubsub.bits(users_oauth_token)[users_channel_id]
    ]
    await client.pubsub.subscribe_topics(topics)
    await client.start()

    @client.event()
    async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
        pass  # do stuff on bit redemptions

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        print(f"Channel point event: {event}")
        pass  # do stuff on channel point redemptions
