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

try:
    from asyncio import run as asyncio_run
except ImportError:
    from discordproxy.runners import run as asyncio_run

logger = logging.getLogger(__name__)
discord.VoiceClient.warn_nacl = False


async def shutdown_server(signal, server, discord_client):
    logger.info("Received shutdown signal: %s", signal)
    logger.info("Logging out from Discord...")
    await discord_client.logout()
    logger.info("Shutting down gRPC service...")
    await server.stop(0)


async def run_server(token: str, my_args) -> None:
    # init gRPC server
    server = grpc.aio.server()
    discord_client = DiscordClient()
    add_DiscordApiServicer_to_server(DiscordApi(discord_client), server)
    listen_addr = f"{my_args.host}:{my_args.port}"
    server.add_insecure_port(listen_addr)
    # add event handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.ensure_future(
                shutdown_server(s, server, discord_client)
            ),
        )

    # start the server
    logger.info("Starting gRPC service on {listen_addr}")
    await server.start()
    asyncio.ensure_future(discord_client.start(token))
    await server.wait_for_termination()
    logger.info("gRPC service has shut down")


def main():
    logger.info(f"Starting {__title__} v{__version__}...")
    token, my_args = setup_server(sys.argv[1:])
    asyncio_run(run_server(token=token, my_args=my_args))


if __name__ == "__main__":
    main()
