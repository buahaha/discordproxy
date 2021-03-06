from random import randint

import grpc

from discordproxy.discord_api_pb2 import (
    DirectMessageRequest,
    Embed,
    # Thumbnail,
    GetGuildChannelsRequest,
)
from discordproxy.discord_api_pb2_grpc import DiscordApiStub


def send_message():
    channel = grpc.insecure_channel("localhost:50051")
    client = DiscordApiStub(channel)
    random_id = randint(1, 1000000000)
    request = DirectMessageRequest(
        user_id=123,  # 152878250039705600,
        content=f"Hi #{random_id}",
        embed=Embed(description="oh yes"),
    )
    try:
        client.SendDirectMessage(request)
    except grpc.RpcError as e:
        print(e.args[0].details)


def get_channels():
    channel = grpc.insecure_channel("localhost:50051")
    client = DiscordApiStub(channel)
    request = GetGuildChannelsRequest(guild_id=123)  # 197097249610661888
    try:
        channels = client.GetGuildChannels(request)
    except grpc.RpcError as e:
        print(e.args[0].code)
        print(e.args[0].details)
    else:
        print(channels)


get_channels()
