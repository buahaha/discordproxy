import grpc

from discordproxy.discord_api_pb2 import (
    SendDirectMessageRequest,
    GetGuildChannelsRequest,
)
from discordproxy.discord_api_pb2_grpc import DiscordApiStub


def send_direct_message(user_id):
    channel = grpc.insecure_channel("localhost:50051")
    client = DiscordApiStub(channel)
    request = SendDirectMessageRequest(user_id=user_id, content="Hey, stranger!")
    try:
        client.SendDirectMessage(request)
    except grpc.RpcError as e:
        print(e.args[0].code)
        print(e.args[0].details)


def get_channels(guild_id):
    channel = grpc.insecure_channel("localhost:50051")
    client = DiscordApiStub(channel)
    request = GetGuildChannelsRequest(guild_id=197097249610661888)
    try:
        channels = client.GetGuildChannels(request)
    except grpc.RpcError as e:
        print(e.args[0].code)
        print(e.args[0].details)
    else:
        print(channels)
