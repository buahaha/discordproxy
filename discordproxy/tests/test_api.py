from unittest.mock import Mock, MagicMock
from aiounittest import AsyncTestCase

import discord
from discord.errors import NotFound, Forbidden
import grpc

from discordproxy import api
from discordproxy import discord_api_pb2


USERS = {1001: "user-1", 1002: "user-2", 1100: "forbidden user"}
USERS_FORBIDDEN = [1100]
CHANNELS = {2001: "channel-1", 2002: "channel-2", 2100: "forbidden channel"}
CHANNELS_FORBIDDEN = [2100]


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class ResponseStub:
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
                response=ResponseStub(403), message="Test:Forbidden channel"
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


class DiscordStub:
    async def fetch_channel(self, channel_id):
        if channel_id in CHANNELS:
            if channel_id in CHANNELS_FORBIDDEN:
                raise Forbidden(response=Mock(), message="Test:Forbidden channel")
            return DiscordChannel(id=channel_id, name=CHANNELS[channel_id])
        raise NotFound(response=ResponseStub(404), message="Test:Unknown channel")

    async def fetch_user(self, user_id):
        if user_id in USERS:
            return DiscordUser(id=user_id, name=USERS[user_id])
        raise NotFound(response=ResponseStub(404), message="Test:Unknown user")


class ServicerContextStub:
    def __init__(self) -> None:
        self._code = grpc.StatusCode.UNKNOWN
        self._details = ""

    def set_code(self, code):
        self._code = code

    def set_details(self, details):
        self._details = details


class TestSendDirectMessage(AsyncTestCase):
    async def test_should_send_message_normally(self):
        # given
        my_api = api.DiscordApi(DiscordStub())
        request = discord_api_pb2.SendDirectMessageRequest()
        request.user_id = 1001
        request.content = "content"
        # when
        result = await my_api.SendDirectMessage(request=request, context=MagicMock())
        # then
        self.assertIsInstance(result, discord_api_pb2.SendDirectMessageResponse)

    async def test_should_return_error_when_user_not_known(self):
        # given
        my_api = api.DiscordApi(DiscordStub())
        request = discord_api_pb2.SendDirectMessageRequest()
        request.user_id = 666
        request.content = "content"
        context = ServicerContextStub()
        # when
        result = await my_api.SendDirectMessage(request, context)
        # then
        self.assertEqual(result, discord_api_pb2.SendDirectMessageResponse())


# class TestPostDirectMessageView(AioHTTPTestCase):
#     async def get_application(self):
#         app = web.Application()
#         app.add_routes(routes)
#         app["discord_client"] = DiscordStub()
#         return app

#     @unittest_run_loop
#     async def test_should_return_204_when_ok_content_only(self):
#         # when
#         resp = await self.client.request(
#             "POST",
#             "/send_direct_message",
#             json={"user_id": 1001, "content": "test_content"},
#         )
#         # then
#         self.assertEqual(resp.status, 204)

#     @unittest_run_loop
#     async def test_should_return_204_when_ok_embed_only(self):
#         # when
#         resp = await self.client.request(
#             "POST",
#             "/send_direct_message",
#             json={"user_id": 1001, "embed": {"description": "dummy"}},
#         )
#         # then
#         self.assertEqual(resp.status, 204)

#     @unittest_run_loop
#     async def test_should_return_204_when_ok_content_and_embed(self):
#         # when
#         resp = await self.client.request(
#             "POST",
#             "/send_direct_message",
#             json={
#                 "user_id": 1001,
#                 "content": "test_content",
#                 "embed": {"description": "dummy"},
#             },
#         )
#         # then
#         self.assertEqual(resp.status, 204)

#     @unittest_run_loop
#     async def test_should_return_400_when_mandatory_param_is_missing(self):
#         # when
#         resp = await self.client.request(
#             "POST",
#             "/send_direct_message",
#             json={"content": "bla bla"},
#         )
#         # then
#         self.assertEqual(resp.status, 400)

#     @unittest_run_loop
#     async def test_should_return_400_when_both_content_and_embed_are_missing(self):
#         # when
#         resp = await self.client.request(
#             "POST", "/send_direct_message", json={"user_id": 1001}
#         )
#         # then
#         self.assertEqual(resp.status, 400)

#     @unittest_run_loop
#     async def test_should_return_404_when_user_is_unknown(self):
#         # when
#         resp = await self.client.request(
#             "POST",
#             "/send_direct_message",
#             json={"user_id": 666, "content": "test_content"},
#         )
#         # then
#         self.assertEqual(resp.status, 404)

#     @unittest_run_loop
#     async def test_should_return_403_when_user_access_not_allowed(self):
#         # when
#         resp = await self.client.request(
#             "POST",
#             "/send_direct_message",
#             json={"user_id": 1100, "content": "test_content"},
#         )
#         # then
#         self.assertEqual(resp.status, 403)
