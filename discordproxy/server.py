import asyncio

import discord
from grpclib.server import Server
from grpclib.utils import graceful_exit

from .api import DiscordApi


async def run_server(*, host: str = "127.0.0.1", port: int = 50051) -> None:
    discord_client = discord.Client()
    server = Server([DiscordApi(discord_client)])
    # Note: graceful_exit isn't supported in Windows
    with graceful_exit([server]):
        await server.start(host, port)
        print(f"Serving on {host}:{port}")
        asyncio.ensure_future(
            discord_client.start(
                "NzI1ODExNzY5ODk2ODYxNzk3.XvULjg.tloTzInV3JOLJEmSK-oLeQtOPzI"
            )
        )
        await server.wait_closed()


def main():
    asyncio.run(run_server())
