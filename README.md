# discordproxy

> **THIS IS WORK-IN-PROGRESS** - Not released for production use yet

Proxy server for accessing the Discord API via gRPC

[![release](https://img.shields.io/pypi/v/discordproxy?label=release)](https://pypi.org/project/discordproxy/)
[![python](https://img.shields.io/pypi/pyversions/discordproxy)](https://pypi.org/project/discordproxy/)
[![pipeline](https://gitlab.com/ErikKalkoken/discordproxy/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/discordproxy/-/pipelines)
[![coverage report](https://gitlab.com/ErikKalkoken/discordproxy/badges/master/coverage.svg)](https://gitlab.com/ErikKalkoken/discordproxy/-/commits/master)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/discordproxy/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Overview

This is a proxy server that provides access to the Discord API via gRPC.

The main purpose is to enable applications to use the Discord API without having to implement Discord's websocket protocol. Instead, they can use the gRPC API and the proxy will resolve all requests with the Discord API server via websockets or HTTP.

Python applications can import the generated gRPC client directly. Applications in other languages can use the protobuf definition to generate their own gRPC client.

## Example

Here is a simple example for sending a direct message to user with ID 123 (without error handling):

```python
import grpc

from discordproxy.discord_api_pb2 import DirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub


channel = grpc.insecure_channel("localhost:50051")
client = DiscordApiStub(channel)
request = DirectMessageRequest(user_id=123, content="This is the way")
client.SendDirectMessage(request)

```

## Error handling

If a gRPC request fails a `grpc.RpcError` exception will be raised. RPC errors return the context of the request, consists of two fields:

- `code`: the [gRPC status code](https://grpc.github.io/grpc/core/md_doc_statuscodes.html)
- `details`: a string with additional details about the error.

The [Discord API](https://discord.com/developers/docs/topics/opcodes-and-status-codes) will return two types of error codes:

- HTTP response code (e.g. 404 if a request user does not exist)
- JSON error code (e.g. 30007 when the maximum number of webhooks is reached )

We have mapped the HTTP response code to gRPC status codes. In addition the details field will contain the full information as JSON object.

### gRPC status codes

HTTP response code | gRPC status code
-- | --
400 (BAD REQUEST) | `INVALID_ARGUMENT`
401 (UNAUTHORIZED) | `UNAUTHENTICATED`
403 (FORBIDDEN) | `PERMISSION_DENIED`
404 (NOT FOUND) | `NOT_FOUND`
405 (METHOD NOT ALLOWED) | `INVALID_ARGUMENT`
429 (TOO MANY REQUESTS) | `RESOURCE_EXHAUSTED`
502 (GATEWAY UNAVAILABLE) | `UNAVAILABLE`
504 (GATEWAY TIMEOUT) | `DEADLINE_EXCEEDED`
5xx (SERVER ERROR) | `INTERNAL`

### gRPC details

gRPC exceptions have a code and a detail property. Discord errors will always have `code = grpc.StatusCode.ABORTED` and contain the actual Discord error in the detail property as JSON object, e.g.:

```json
{
    "type": "HTTPException",
    "status": 403,
    "code": 50001,
    "text": "Missing Access"
}
```

Legend:

- `status`: HTTP status code
- `code`: JSON error code
- `text`: Error message

### Example

Here is an example on how to get details for errors from your gRPC calls:

```python
try:
    client.SendDirectMessage(request)
except grpc.RpcError as e:
    print(e.args[0].code)
    print(e.args[0].details)
```

> **Note**<br>While this example only looks at the first element, `e.args` might actually contain more than one error.
