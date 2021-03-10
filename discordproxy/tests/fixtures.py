from unittest.mock import MagicMock

import discord
from discord.errors import NotFound, Forbidden
import grpc


mock_state = MagicMock(name="ConnectionState")
mock_state.store_user = lambda data: discord.User(state=mock_state, data=data)
CHANNEL_TYPE_GUILD_TEXT = 0


def obj_list_2_dict(obj_list) -> dict:
    """converts a list of Discord object to a dict with the ID as key"""
    return {obj.id: obj for obj in obj_list}


def obj_dict_by_id(obj_list) -> dict:
    return {obj["id"]: obj for obj in obj_list}


USERS_DATA = [
    {
        # this is the bot used by discordproxy on Discord
        "id": 1001,
        "username": "my_bot",
        "discriminator": "my_bot-discriminator",
        "avatar": "my_bot-avatar",
        "bot": True,
    },
    {
        "id": 1002,
        "username": "user-2",
        "discriminator": "discriminator-2",
        "avatar": "avatar-2",
    },
    {
        "id": 1100,
        "username": "user-forbidden",
        "discriminator": "discriminator-forbidden",
        "avatar": "avatar-forbidden",
    },
]
USERS_DATA_BY_ID = obj_dict_by_id(USERS_DATA)
USERS = obj_list_2_dict(
    [discord.User(state=mock_state, data=data) for data in USERS_DATA]
)
USERS_FORBIDDEN = [1100]
GUILDS = obj_list_2_dict(
    [
        # this is the current guild
        discord.Guild(data={"id": 3001, "name": "Alpha"}, state=mock_state)
    ]
)
CHANNELS = obj_list_2_dict(
    [
        discord.TextChannel(
            state=mock_state,
            guild=GUILDS[3001],
            data={
                "id": 2001,
                "name": "channel-1",
                "type": CHANNEL_TYPE_GUILD_TEXT,
                "position": 1,
            },
        ),
        discord.TextChannel(
            state=mock_state,
            guild=GUILDS[3001],
            data={
                "id": 2002,
                "name": "channel-2",
                "type": CHANNEL_TYPE_GUILD_TEXT,
                "position": 2,
            },
        ),
        discord.DMChannel(
            state=mock_state,
            me=False,
            data={"id": 2010, "recipients": [USERS_DATA_BY_ID[1002]]},
        ),
        discord.TextChannel(
            state=mock_state,
            guild=GUILDS[3001],
            data={
                "id": 2100,
                "name": "channel-forbidden",
                "type": CHANNEL_TYPE_GUILD_TEXT,
                "position": 3,
            },
        ),
    ]
)
CHANNELS_FORBIDDEN = [2100]
ROLES = obj_list_2_dict(
    [
        discord.Role(
            state=mock_state,
            guild=GUILDS[3001],
            data={"id": 1, "name": "role-1"},
        ),
        discord.Role(
            state=mock_state,
            guild=GUILDS[3001],
            data={"id": 2, "name": "role-2"},
        ),
    ]
)
MEMBERS_DATA = [{"user": USERS_DATA_BY_ID[1001], "roles": [1, 2]}]
MEMBERS_DATA_BY_ID = {obj["user"]["id"]: obj for obj in MEMBERS_DATA}
MEMBERS_LIST = [
    discord.Member(data=data, guild=GUILDS[3001], state=mock_state)
    for data in MEMBERS_DATA
]

MEMBERS = obj_list_2_dict(MEMBERS_LIST)


class DiscordClientResponseStub:
    def __init__(self, status=200, reason="") -> None:
        self.status = status
        self.reason = reason


class DiscordChannel:
    def __init__(self, id) -> None:
        self.channel = CHANNELS[id]

    async def send(self, content, embed=None):
        if content:
            assert isinstance(content, str)
        if embed:
            assert isinstance(embed, discord.Embed)
        if self.channel.id in CHANNELS_FORBIDDEN:
            raise Forbidden(
                response=DiscordClientResponseStub(403),
                message="Test:Forbidden channel",
            )

        data = {
            "id": 42,
            "channel_id": self.channel.id,
            "type": 0,
            "content": content,
            "mention_everyone": False,
            "timestamp": "2021-03-09T18:25:42.081000+00:00",
            "edited_timestamp": "2021-03-09T18:25:42.081000+00:00",
            "tts": False,
            "pinned": False,
            "attachments": [],
            "embeds": [embed.to_dict()] if embed else [],
            "author": USERS_DATA_BY_ID[1001],
        }
        if isinstance(self.channel, discord.TextChannel):
            data["guild_id"] = self.channel.guild.id
            data["member"] = MEMBERS_DATA_BY_ID[1001]

        return discord.Message(state=mock_state, channel=self.channel, data=data)


class DiscordUser:
    def __init__(self, id) -> None:
        self.user = USERS[id]

    async def create_dm(self):
        if self.user.id in USERS_FORBIDDEN:
            return DiscordChannel(2100)
        else:
            return DiscordChannel(2010)


class DiscordGuild:
    def __init__(self, id) -> None:
        self.guild = GUILDS[id]

    async def fetch_channels(self) -> list:
        return [
            channel
            for channel in CHANNELS.values()
            if isinstance(channel, discord.TextChannel) and channel.guild == self.guild
        ]


class DiscordClientStub:
    async def start(self, *args, **kwargs):
        pass

    async def logout(self):
        pass

    async def fetch_channel(self, channel_id):
        if channel_id in CHANNELS:
            if channel_id in CHANNELS_FORBIDDEN:
                raise Forbidden(
                    response=DiscordClientResponseStub(403), message="Forbidden channel"
                )
            return DiscordChannel(id=channel_id)
        raise NotFound(
            response=DiscordClientResponseStub(404), message="Unknown channel"
        )

    async def fetch_user(self, user_id):
        if user_id in USERS:
            return DiscordUser(id=user_id)
        raise NotFound(response=DiscordClientResponseStub(404), message="Unknown user")

    async def fetch_guild(self, guild_id):
        if guild_id in GUILDS:
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
