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
discord.VoiceClient.warn_nacl = False


async def shutdown_server(signal, server, discord_client):
    logger.info("Received shutdown signal: %s", signal)
    logger.info("Logging out from Discord...")
    await discord_client.logout()
    logger.info("Shutting down gRPC server...")
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
            lambda s=s: asyncio.create_task(shutdown_server(s, server, discord_client)),
        )

    # start the server
    msg = f"Starting gRPC server on {listen_addr}"
    logger.info("%s", msg)
    print(msg)
    await server.start()
    asyncio.ensure_future(discord_client.start(token))
    await server.wait_for_termination()
    msg = "gRPC server has shut down"
    logger.info("%s", msg)
    print(msg)


def main():
    logger.info(f"Starting {__title__} v{__version__}...")
    print(f"{__title__} v{__version__}")
    print()
    token, my_args = setup_server(sys.argv[1:])
    asyncio.run(run_server(token=token, my_args=my_args))


if __name__ == "__main__":
    main()
