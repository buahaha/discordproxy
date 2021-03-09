from unittest.mock import MagicMock

import discord
from discord.errors import NotFound, Forbidden
import grpc

from . import testdata


def my_handle_author(self, data):
    self.author = discord.User(
        state=MagicMock(spec=discord.state.ConnectionState), data=data
    )


discord.Message._handle_author = my_handle_author


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class DiscordClientResponseStub:
    def __init__(self, status=200, reason="") -> None:
        self.status = status
        self.reason = reason


class DiscordChannel:
    def __init__(self, id) -> None:
        self.channel = testdata.CHANNELS[id]

    async def send(self, content, embed=None):
        if content:
            assert isinstance(content, str)
        if embed:
            assert isinstance(embed, discord.Embed)
        if self.channel.id in testdata.CHANNELS_FORBIDDEN:
            raise Forbidden(
                response=DiscordClientResponseStub(403),
                message="Test:Forbidden channel",
            )
        return discord.Message(
            state=testdata.mock_state(),
            channel=self.channel,
            data={
                "id": 42,
                "type": 0,
                "content": content,
                "mention_everyone": False,
                "timestamp": "2021-03-09T18:25:42.081000+00:00",
                "edited_timestamp": "2021-03-09T18:25:42.081000+00:00",
                "tts": False,
                "pinned": False,
                "attachments": [],
                "embeds": [],  # TODO: convert embeds to dicts
                "author": {
                    "id": 1001,
                    "username": "user-1",
                    "discriminator": "discriminator-1",
                    "avatar": "avatar-1",
                },
            },
        )


class DiscordUser:
    def __init__(self, id) -> None:
        self.user = testdata.USERS[id]

    async def create_dm(self):
        if self.user.id in testdata.USERS_FORBIDDEN:
            return DiscordChannel(2100)
        else:
            return DiscordChannel(2010)


class DiscordGuild:
    def __init__(self, id) -> None:
        self.guild = testdata.GUILDS[id]

    async def fetch_channels(self) -> list:
        return [
            channel
            for channel in testdata.CHANNELS.values()
            if isinstance(channel, discord.TextChannel) and channel.guild == self.guild
        ]


class DiscordClientStub:
    async def start(self, *args, **kwargs):
        pass

    async def logout(self):
        pass

    async def fetch_channel(self, channel_id):
        if channel_id in testdata.CHANNELS:
            if channel_id in testdata.CHANNELS_FORBIDDEN:
                raise Forbidden(
                    response=DiscordClientResponseStub(403), message="Forbidden channel"
                )
            return DiscordChannel(id=channel_id)
        raise NotFound(
            response=DiscordClientResponseStub(404), message="Unknown channel"
        )

    async def fetch_user(self, user_id):
        if user_id in testdata.USERS:
            return DiscordUser(id=user_id)
        raise NotFound(response=DiscordClientResponseStub(404), message="Unknown user")

    async def fetch_guild(self, guild_id):
        if guild_id in testdata.GUILDS:
            return DiscordGuild(id=guild_id)
        raise NotFound(response=DiscordClientResponseStub(404), message="Unknown guild")


class ServicerContextStub:
    def __init__(self) -> None:
        self._code = grpc.StatusCode.UNKNOWN
        self._details = ""

    def set_code(self, code):
        self._code = code

    def set_details(self, details):
        self._details = details
