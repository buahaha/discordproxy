from random import randint

import grpc

from discordproxy.grpc_sync.discord_api_pb2 import (
    DirectMessageRequest,
    Embed,
    # Thumbnail,
    GetGuildChannelsRequest,
)
from discordproxy.grpc_sync.discord_api_pb2_grpc import DiscordApiStub


def send_message():
    channel = grpc.insecure_channel("localhost:50051")
    client = DiscordApiStub(channel)
    random_id = randint(1, 1000000000)
    request = DirectMessageRequest(
        user_id=152878250039705600,
        content=f"Hi #{random_id}",
        embed=Embed(description="oh yes"),
    )
    client.SendDirectMessage(request)


def get_channels():
    channel = grpc.insecure_channel("localhost:50051")
    client = DiscordApiStub(channel)
    request = GetGuildChannelsRequest(guild_id=197097249610661888)
    channels = client.GetGuildChannels(request)
    print(channels)


send_message()
