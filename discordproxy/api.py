import functools

import discord
from google.protobuf import json_format
import grpc
import json

from discordproxy import discord_api_pb2_grpc
from discordproxy import discord_api_pb2


def handle_discord_exceptions(Response):
    """converts discord HTTP exceptions into gRPC context"""

    def wrapper(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except discord.errors.HTTPException as ex:
                details = {
                    "type": "HTTPException",
                    "status": ex.status,
                    "code": ex.code,
                    "text": ex.text,
                }
                context = args[2]
                context.set_code(grpc.StatusCode.ABORTED)
                context.set_details(json.dumps(details))
                return Response()

        return decorated

    return wrapper


class DiscordApi(discord_api_pb2_grpc.DiscordApiServicer):
    def __init__(self, discord_client) -> None:
        super().__init__()
        self.discord_client = discord_client

    @handle_discord_exceptions(discord_api_pb2.SendDirectMessageResponse)
    async def SendDirectMessage(
        self, request: discord_api_pb2.SendDirectMessageRequest, context
    ) -> discord_api_pb2.SendDirectMessageResponse:
        user = await self.discord_client.fetch_user(user_id=request.user_id)
        channel = await user.create_dm()
        if request.embed.ByteSize():
            embed_dct = json_format.MessageToDict(request.embed)
            embed = discord.Embed.from_dict(embed_dct)
        else:
            embed = None
        await channel.send(content=request.content, embed=embed)
        return discord_api_pb2.SendDirectMessageResponse()

    @handle_discord_exceptions(discord_api_pb2.GetGuildChannelsResponse)
    async def GetGuildChannels(self, request, context):
        guild = await self.discord_client.fetch_guild(request.guild_id)
        channels = await guild.fetch_channels()
        channels_2 = [
            discord_api_pb2.Channel(id=channel.id, name=channel.name)
            for channel in channels
        ]
        return discord_api_pb2.GetGuildChannelsResponse(channels=channels_2)
