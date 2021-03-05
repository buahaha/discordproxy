import asyncio
import argparse
import logging
import logging.config
import os
from pathlib import Path
import sys

from . import __title__, __version__, constants
import discord
from grpclib.server import Server
from grpclib.utils import graceful_exit

from .api import DiscordApi

logger = logging.getLogger(__name__)
_LOG_FILE_NAME = "discordproxyserver.log"


def setup_server(args_list: list) -> tuple:
    """parses all command line arguments and configures logging"""
    my_args = _parse_args(args_list)
    token = (
        os.environ.get("DISCORD_BOT_TOKEN") if my_args.token is None else my_args.token
    )
    if not token:
        print("ERROR: No Discord bot token provided")
        exit(1)
    logging.config.dictConfig(_logging_config(my_args))
    return token, my_args


def _parse_args(args_list: list) -> argparse.ArgumentParser:
    """returns parsed command line arguments"""
    my_arg_parser = argparse.ArgumentParser(
        description="Server with HTTP API for sending messages to Discord",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    my_arg_parser.add_argument(
        "--token",
        help=(
            "Discord bot token. Can alternatively be specified as "
            "environment variable DISCORD_BOT_TOKEN."
        ),
    )
    my_arg_parser.add_argument(
        "--host", default=constants.DEFAULT_HOST, help="server host address"
    )
    my_arg_parser.add_argument(
        "--port", type=int, default=constants.DEFAULT_PORT, help="server port"
    )
    my_arg_parser.add_argument(
        "--log-level",
        default="INFO",
        help="Log level of log file",
        choices=["INFO", "WARN", "ERROR", "CRITICAL"],
    )
    my_arg_parser.add_argument(
        "--log-file-path",
        help=(
            "Path for storing the log file. If no path if provided, "
            "the log file will be stored in the current working folder"
        ),
    )
    my_arg_parser.add_argument(
        "--version",
        help="show the program version and exit",
        action="version",
        version=__version__,
    )
    return my_arg_parser.parse_args(args_list)


def _logging_config(my_args) -> dict:
    """returns dict to configure logging based on parsed args"""
    file_log_path_full = my_args.log_file_path
    filename = (
        Path(file_log_path_full) / _LOG_FILE_NAME
        if file_log_path_full
        else Path.cwd() / _LOG_FILE_NAME
    )
    print(f"Writing logfile to: {filename}")
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "[%(levelname)s] %(message)s"},
            "file": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "CRITICAL",
                "formatter": "console",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
            "file": {
                "level": my_args.log_level,
                "formatter": "file",
                "class": "logging.FileHandler",
                "filename": str(filename),
                "mode": "a",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


class MyClient(discord.Client):
    """Custom sub-class for handling Discord events"""

    async def on_connect(self):
        logger.info("%s has connected to Discord", self.user.name)

    async def on_ready(self):
        logger.info("%s as logged in successfully", self.user.name)

    async def on_disconnect(self):
        logger.info("%s has disconnected from Discord", self.user.name)


async def run_server(token, my_args) -> None:
    logger.info(f"Starting {__title__} v{__version__}...")
    discord.VoiceClient.warn_nacl = False
    discord_client = MyClient()
    server = Server([DiscordApi(discord_client)])
    with graceful_exit([server]):
        try:
            await server.start(my_args.host, my_args.port)
            msg = f"Running gRPC server on {my_args.host}:{my_args.port}"
            logger.info(msg)
            print(msg)
            asyncio.ensure_future(discord_client.start(token))
            await server.wait_closed()
            logger.info("gRPC server has shut down")
        finally:
            logger.info("Logging out from Discord...")
            await discord_client.logout()


def main():
    print(f"{__title__} v{__version__}")
    print()
    asyncio.run(run_server(*setup_server(sys.argv[1:])))
