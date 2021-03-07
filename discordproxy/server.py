import asyncio
import logging
import signal
import sys

import discord
import grpc

from discordproxy import __title__, __version__
from discordproxy.discord_api_pb2_grpc import add_DiscordApiServicer_to_server
from discordproxy.api import DiscordApi
from discordproxy.config import setup_server
from discordproxy.discord_client import DiscordClient

logger = logging.getLogger(__name__)


async def shutdown_server(signal, server, discord_client):
    logger.info("Received shutdown signal: %s", signal)
    logger.info("Logging out from Discord...")
    await discord_client.logout()
    logger.info("Shutting down gRPC server...")
    await server.stop(0)


async def run_server(token, my_args) -> None:
    # init gRPC server and discord client
    logger.info(f"Starting {__title__} v{__version__}...")
    discord.VoiceClient.warn_nacl = False
    discord_client = DiscordClient()
    server = grpc.aio.server()
    add_DiscordApiServicer_to_server(DiscordApi(discord_client), server)
    listen_addr = f"{my_args.host}:{my_args.port}"
    server.add_insecure_port(listen_addr)

    # add event handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(shutdown_server(s, server, discord_client)),
        )

    # start the server
    msg = f"Starting gRPC server on {listen_addr}"
    logger.info(msg)
    print(msg)
    await server.start()
    asyncio.ensure_future(discord_client.start(token))
    await server.wait_for_termination()
    logger.info("gRPC server has shut down")


def main():
    print(f"{__title__} v{__version__}")
    print()
    asyncio.run(run_server(*setup_server(sys.argv[1:])))


if __name__ == "__main__":
    main()
