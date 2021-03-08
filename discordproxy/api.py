import functools

import discord
from google.protobuf import json_format
import grpc
import json

from discordproxy import discord_api_pb2_grpc
from discordproxy import discord_api_pb2


def _gen_grpc_details(status: int, code: int, text: str):
    return {
        "type": "HTTPException",
        "status": int(status),
        "code": int(code),
        "text": str(text),
    }


def handle_discord_exceptions(Response):
    """converts discord HTTP exceptions into gRPC context"""

    _CODES_MAPPING = {
        400: grpc.StatusCode.INVALID_ARGUMENT,
        401: grpc.StatusCode.UNAUTHENTICATED,
        403: grpc.StatusCode.PERMISSION_DENIED,
        404: grpc.StatusCode.NOT_FOUND,
        405: grpc.StatusCode.INVALID_ARGUMENT,
        429: grpc.StatusCode.RESOURCE_EXHAUSTED,
        500: grpc.StatusCode.INTERNAL,
        502: grpc.StatusCode.UNAVAILABLE,
        504: grpc.StatusCode.DEADLINE_EXCEEDED,
    }

    def wrapper(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except discord.errors.HTTPException as ex:
                details = _gen_grpc_details(
                    status=ex.status, code=ex.code, text=ex.text
                )
                context = args[2]
                context.set_code(_CODES_MAPPING.get(ex.status, grpc.StatusCode.UNKNOWN))
                context.set_details(json.dumps(details))
                return Response()

        return decorated

    return wrapper


class DiscordApi(discord_api_pb2_grpc.DiscordApiServicer):
    def __init__(self, discord_client) -> None:
        super().__init__()
        self.discord_client = discord_client

    @handle_discord_exceptions(discord_api_pb2.SendDirectMessageResponse)
    async def SendDirectMessage(self, request, context):
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
