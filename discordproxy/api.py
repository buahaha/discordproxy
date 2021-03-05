import functools

import discord
from google.protobuf import json_format
from grpclib.exceptions import GRPCError, Status
from grpclib.server import Stream

from .grpc_async.discord_api_grpc import DiscordApiBase
from .grpc_async.discord_api_pb2 import (
    DirectMessageRequest,
    DiscordReply,
    GetGuildChannelsRequest,
    GetGuildChannelsResponse,
    Channel,
)


def handle_discord_exceptions(func):
    """converts discord HTTP exceptions into GRPC exceptions"""

    @functools.wraps(func)
    async def decorated(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except discord.errors.DiscordException as ex:
            raise GRPCError(status=Status.ABORTED, message=str(ex))

    return decorated


class DiscordApi(DiscordApiBase):
    def __init__(self, discord_client) -> None:
        super().__init__()
        self.discord_client = discord_client

    @handle_discord_exceptions
    async def SendDirectMessage(
        self, stream: Stream[DirectMessageRequest, DiscordReply]
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        user = await self.discord_client.fetch_user(user_id=request.user_id)
        channel = await user.create_dm()
        if request.embed.ByteSize():
            embed_dct = json_format.MessageToDict(request.embed)
            embed = discord.Embed.from_dict(embed_dct)
        else:
            embed = None
        await channel.send(content=request.content, embed=embed)
        await stream.send_message(DiscordReply(ok=True, message="looks good"))

    @handle_discord_exceptions
    async def GetGuildChannels(
        self, stream: Stream[GetGuildChannelsRequest, GetGuildChannelsResponse]
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        guild = await self.discord_client.fetch_guild(request.guild_id)
        channels = await guild.fetch_channels()
        channels_2 = [Channel(id=channel.id, name=channel.name) for channel in channels]
        await stream.send_message(GetGuildChannelsResponse(channels=channels_2))
