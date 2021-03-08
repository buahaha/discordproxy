# from time import sleep
# import unittest
# import asyncio
# from collections import namedtuple

# from aiounittest import AsyncTestCase
# import grpc

# from discordproxy.discord_api_pb2 import SendDirectMessageRequest
# from discordproxy.discord_api_pb2_grpc import DiscordApiStub
# from discordproxy.server import run_server
# from .helpers import DiscordClientStub


# MyArgsStub = namedtuple("MyArgsStub", ["host", "port"])


# class TestEnd2End(unittest.TestCase):
#     def setUp(self) -> None:
#         self.host = "127.0.0.1"
#         self.port = 50051
#         token = "dummy"
#         my_args = MyArgsStub(host=self.host, port=self.port)
#         discord_client = DiscordClientStub()
#         self.loop = asyncio.get_event_loop()
#         self.loop.run_until_complete(
#             run_server(token=token, my_args=my_args, discord_client=discord_client)
#         )

#     def tearDown(self) -> None:
#         self.loop.close()

#     def test_make_call(self):
#         sleep(5)
#         channel = grpc.insecure_channel(f"{self.host}:{self.port}")
#         client = DiscordApiStub(channel)
#         request = SendDirectMessageRequest(user_id=1001, content="content")
#         client.SendDirectMessage(request)
