# import functools

import discord
from google.protobuf import json_format

from discordproxy.grpc_api import discord_api_pb2_grpc
from discordproxy.grpc_api import discord_api_pb2

# def handle_discord_exceptions(func):
#     """converts discord HTTP exceptions into GRPC exceptions"""

#     @functools.wraps(func)
#     async def decorated(*args, **kwargs):
#         try:
#             return await func(*args, **kwargs)
#         except discord.errors.DiscordException as ex:
#             raise GRPCError(status=Status.ABORTED, message=str(ex))

#     return decorated


class DiscordApi(discord_api_pb2_grpc.DiscordApiServicer):
    def __init__(self, discord_client) -> None:
        super().__init__()
        self.discord_client = discord_client

    async def SendDirectMessage(self, request, context):
        user = await self.discord_client.fetch_user(user_id=request.user_id)
        channel = await user.create_dm()
        if request.embed.ByteSize():
            embed_dct = json_format.MessageToDict(request.embed)
            embed = discord.Embed.from_dict(embed_dct)
        else:
            embed = None
        await channel.send(content=request.content, embed=embed)
        return discord_api_pb2.DiscordReply(ok=True, message="looks good")

    async def GetGuildChannels(self, request, context):
        guild = await self.discord_client.fetch_guild(request.guild_id)
        channels = await guild.fetch_channels()
        channels_2 = [
            discord_api_pb2.Channel(id=channel.id, name=channel.name)
            for channel in channels
        ]
        return discord_api_pb2.GetGuildChannelsResponse(channels=channels_2)
