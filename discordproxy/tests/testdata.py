from unittest.mock import MagicMock
import discord


mock_state = MagicMock(spec=discord.state.ConnectionState)

CHANNEL_TYPE_GUILD_TEXT = 0

USERS = {
    1001: discord.User(
        state=mock_state(),
        data={
            "id": 1001,
            "username": "user-1",
            "discriminator": "discriminator-1",
            "avatar": "avatar-1",
        },
    ),
    1002: discord.User(
        state=mock_state(),
        data={
            "id": 1002,
            "username": "user-2",
            "discriminator": "discriminator-2",
            "avatar": "avatar-2",
        },
    ),
    1100: discord.User(
        state=mock_state(),
        data={
            "id": 1100,
            "username": "user-forbidden",
            "discriminator": "discriminator-forbidden",
            "avatar": "avatar-forbidden",
        },
    ),
}
USERS_FORBIDDEN = [1100]
GUILDS = {3001: discord.Guild(data={"id": 3001, "name": "Alpha"}, state=mock_state())}
CHANNELS = {
    2001: discord.TextChannel(
        state=mock_state(),
        guild=GUILDS[3001],
        data={
            "id": 2001,
            "name": "channel-1",
            "type": CHANNEL_TYPE_GUILD_TEXT,
            "position": 1,
        },
    ),
    2002: discord.TextChannel(
        state=mock_state(),
        guild=GUILDS[3001],
        data={
            "id": 2002,
            "name": "channel-2",
            "type": CHANNEL_TYPE_GUILD_TEXT,
            "position": 2,
        },
    ),
    2010: discord.DMChannel(
        state=mock_state(),
        me=False,
        data={"id": 2010, "recipients": [USERS[1002]]},
    ),
    2100: discord.TextChannel(
        state=mock_state(),
        guild=GUILDS[3001],
        data={
            "id": 2100,
            "name": "channel-forbidden",
            "type": CHANNEL_TYPE_GUILD_TEXT,
            "position": 3,
        },
    ),
}
CHANNELS_FORBIDDEN = [2100]
