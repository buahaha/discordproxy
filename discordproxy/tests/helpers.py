from unittest.mock import Mock, MagicMock

import discord
from discord.errors import NotFound, Forbidden
import grpc

USERS = {1001: "user-1", 1002: "user-2", 1100: "forbidden user"}
USERS_FORBIDDEN = [1100]
CHANNELS = {2001: "channel-1", 2002: "channel-2", 2100: "forbidden channel"}
CHANNELS_FORBIDDEN = [2100]
GUILDS = {3001: {"name": "Alpha", "channels": [2001, 2002]}}


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class DiscordClientResponseStub:
    def __init__(self, status=200, reason="") -> None:
        self.status = status
        self.reason = reason


class DiscordChannel:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    async def send(self, content, embed=None):
        if content:
            assert isinstance(content, str)
        if embed:
            assert isinstance(embed, discord.Embed)
        if self.id in CHANNELS_FORBIDDEN:
            raise Forbidden(
                response=DiscordClientResponseStub(403),
                message="Test:Forbidden channel",
            )


class DiscordUser:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    async def create_dm(self):
        if self.id in USERS_FORBIDDEN:
            return DiscordChannel(2100, "dm-2")
        else:
            return DiscordChannel(2101, "dm-1")


class DiscordGuild:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    async def fetch_channels(self) -> list:
        return [
            DiscordChannel(id=channel_id, name=CHANNELS[channel_id])
            for channel_id in GUILDS[self.id]["channels"]
        ]


class DiscordClientStub:
    async def start(self, *args, **kwargs):
        pass

    async def logout(self):
        pass

    async def fetch_channel(self, channel_id):
        if channel_id in CHANNELS:
            if channel_id in CHANNELS_FORBIDDEN:
                raise Forbidden(response=Mock(), message="Forbidden channel")
            return DiscordChannel(id=channel_id, name=CHANNELS[channel_id])
        raise NotFound(
            response=DiscordClientResponseStub(404), message="Unknown channel"
        )

    async def fetch_user(self, user_id):
        if user_id in USERS:
            return DiscordUser(id=user_id, name=USERS[user_id])
        raise NotFound(response=DiscordClientResponseStub(404), message="Unknown user")

    async def fetch_guild(self, guild_id):
        if guild_id in GUILDS:
            return DiscordGuild(id=guild_id, name=GUILDS[guild_id]["name"])
        raise NotFound(response=DiscordClientResponseStub(404), message="Unknown guild")


class ServicerContextStub:
    def __init__(self) -> None:
        self._code = grpc.StatusCode.UNKNOWN
        self._details = ""

    def set_code(self, code):
        self._code = code

    def set_details(self, details):
        self._details = details
