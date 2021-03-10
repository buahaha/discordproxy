import json
import logging

# from unittest.mock import MagicMock

# from aiounittest import AsyncTestCase
from asynctest import TestCase
import discord
from google.protobuf import json_format
import grpc

from discordproxy import api
from discordproxy import discord_api_pb2
from .fixtures import DiscordClientStub, DiscordClientResponseStub, ServicerContextStub


logging.basicConfig()


class DiscordClientErrorStub(DiscordClientStub):
    """Stub for testing maping of Discord errors to gRPC errors"""

    def __init__(self, status_code, message="") -> None:
        self._status_code = status_code
        self._message = message

    async def fetch_user(self, *args, **kwargs):
        raise discord.errors.HTTPException(
            response=DiscordClientResponseStub(self._status_code), message=self._message
        )


class TestMapDiscordErrors(TestCase):
    def setUp(self) -> None:
        self.request = discord_api_pb2.SendDirectMessageRequest(
            user_id=666, content="content"
        )
        self.context = ServicerContextStub()

    async def test_should_map_all_http_codes_to_grpc_codes(self):
        codes_mapping = {
            400: grpc.StatusCode.INVALID_ARGUMENT,
            401: grpc.StatusCode.UNAUTHENTICATED,
            403: grpc.StatusCode.PERMISSION_DENIED,
            404: grpc.StatusCode.NOT_FOUND,
            405: grpc.StatusCode.INVALID_ARGUMENT,
            429: grpc.StatusCode.RESOURCE_EXHAUSTED,
            500: grpc.StatusCode.INTERNAL,
            502: grpc.StatusCode.UNAVAILABLE,
            504: grpc.StatusCode.DEADLINE_EXCEEDED,
            599: grpc.StatusCode.UNKNOWN,
        }
        for status_code, grpc_code in codes_mapping.items():
            # given
            my_api = api.DiscordApi(DiscordClientErrorStub(status_code))
            # when
            result = await my_api.SendDirectMessage(self.request, self.context)
            # then
            self.assertEqual(result, discord_api_pb2.SendDirectMessageResponse())
            self.assertEqual(self.context._code, grpc_code)
            details = json.loads(self.context._details)
            self.assertEqual(details["status"], status_code)
            self.assertEqual(details["code"], 0)

    async def test_should_return_error_details(self):
        # given
        my_api = api.DiscordApi(DiscordClientErrorStub(404, "my_message"))
        # when
        await my_api.SendDirectMessage(self.request, self.context)
        # then
        details = json.loads(self.context._details)
        self.assertEqual(details["status"], 404)
        self.assertEqual(details["code"], 0)
        self.assertEqual(details["text"], "my_message")


class TestApi(TestCase):
    def setUp(self) -> None:
        self.my_api = api.DiscordApi(DiscordClientStub())
        self.context = ServicerContextStub()

    async def test_should_send_direct_message(self):
        # given
        request = discord_api_pb2.SendDirectMessageRequest(
            user_id=1001, content="content"
        )
        # when
        result = await self.my_api.SendDirectMessage(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.SendDirectMessageResponse)

    async def test_should_send_direct_message_with_embed(self):
        # given
        request = discord_api_pb2.SendDirectMessageRequest(
            user_id=1001,
            content="content",
            embed=discord_api_pb2.Embed(
                title="title",
                type="rich",
                description="description",
                url="url",
                timestamp="2021-03-09T18:25:42.081000+00:00",
                color=0,
                footer=discord_api_pb2.Embed.Footer(
                    text="text", icon_url="icon_url", proxy_icon_url="proxy_icon_url"
                ),
                image=discord_api_pb2.Embed.Image(
                    url="url", proxy_icon_url="proxy_icon_url", height=42, width=66
                ),
                thumbnail=discord_api_pb2.Embed.Thumbnail(
                    url="url", proxy_url="proxy_url", height=42, width=66
                ),
                video=discord_api_pb2.Embed.Video(
                    url="url", proxy_icon_url="proxy_icon_url", height=42, width=66
                ),
                provider=discord_api_pb2.Embed.Provider(name="name", url="url"),
                author=discord_api_pb2.Embed.Author(
                    name="name",
                    url="url",
                    icon_url="icon_url",
                    proxy_icon_url="proxy_icon_url",
                ),
                fields=[
                    discord_api_pb2.Embed.Field(name="name", value="value", inline=True)
                ],
            ),
        )
        # when
        result = await self.my_api.SendDirectMessage(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.SendDirectMessageResponse)

    async def test_should_get_guild_channels(self):
        # given
        request = discord_api_pb2.GetGuildChannelsRequest(guild_id=3001)
        # when
        result = await self.my_api.GetGuildChannels(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.GetGuildChannelsResponse)


class TestDiscordEmbed(TestCase):
    def test_dict_serialization(self):
        # given
        embed_message = discord_api_pb2.Embed(
            title="title",
            type="rich",
            description="description",
            url="url",
            timestamp="2021-03-09T18:25:42.081000+00:00",
            color=0,
            footer=discord_api_pb2.Embed.Footer(
                text="text", icon_url="icon_url", proxy_icon_url="proxy_icon_url"
            ),
            image=discord_api_pb2.Embed.Image(
                url="url", proxy_icon_url="proxy_icon_url", height=42, width=66
            ),
            thumbnail=discord_api_pb2.Embed.Thumbnail(
                url="url", proxy_url="proxy_url", height=42, width=66
            ),
            video=discord_api_pb2.Embed.Video(
                url="url", proxy_icon_url="proxy_icon_url", height=42, width=66
            ),
            provider=discord_api_pb2.Embed.Provider(name="name", url="url"),
            author=discord_api_pb2.Embed.Author(
                name="name",
                url="url",
                icon_url="icon_url",
                proxy_icon_url="proxy_icon_url",
            ),
            fields=[
                discord_api_pb2.Embed.Field(name="name", value="value", inline=True)
            ],
        )
        embed_dict_1 = json_format.MessageToDict(embed_message)
        embed = discord.Embed.from_dict(embed_dict_1)
        # when
        embed_dict_2 = embed.to_dict()
        # then
        self.assertDictEqual(embed_dict_1, embed_dict_2)
