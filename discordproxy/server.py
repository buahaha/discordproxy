import asyncio
import logging
import sys

import discord
import grpc

from discordproxy import __title__, __version__
from discordproxy.discord_api_pb2_grpc import add_DiscordApiServicer_to_server
from discordproxy.api import DiscordApi
from discordproxy.config import setup_server
from discordproxy.discord_client import DiscordClient

logger = logging.getLogger(__name__)


async def run_server(token, my_args) -> None:
    logger.info(f"Starting {__title__} v{__version__}...")
    discord.VoiceClient.warn_nacl = False
    discord_client = DiscordClient()
    server = grpc.aio.server()
    add_DiscordApiServicer_to_server(DiscordApi(discord_client), server)
    listen_addr = f"{my_args.host}:{my_args.port}"
    server.add_insecure_port(listen_addr)
    msg = f"Starting gRPC server on {listen_addr}"
    logger.info(msg)
    print(msg)
    await server.start()
    asyncio.ensure_future(discord_client.start(token))
    try:
        await server.wait_for_termination()
        logger.info("gRPC server has shut down")
    except (SystemExit, KeyboardInterrupt):
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)
    finally:
        await discord_client.logout()
        logger.info("Logged out from Discord")


def main():
    print(f"{__title__} v{__version__}")
    print()
    asyncio.run(run_server(*setup_server(sys.argv[1:])))


if __name__ == "__main__":
    main()
