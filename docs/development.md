# Developer Guide

## Example

Here is a simple example for sending a direct message to user with ID 123 (without error handling):

```python
import grpc

from discordproxy.discord_api_pb2 import DirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub


with grpc.insecure_channel("localhost:50051") as channel:
    client = DiscordApiStub(channel)
    request = DirectMessageRequest(user_id=123, content="This is the way")
    client.SendDirectMessage(request)

```

## Error handling

If a gRPC request fails a `grpc.RpcError` exception will be raised. RPC errors return the context of the request, consisting of two fields:

- `code`: the [gRPC status code](https://grpc.github.io/grpc/core/md_doc_statuscodes.html)
- `details`: a string with additional details about the error.

The [Discord API](https://discord.com/developers/docs/topics/opcodes-and-status-codes) will return two types of error codes:

- HTTP response code (e.g. 404 if a request user does not exist)
- JSON error code (e.g. 30007 when the maximum number of webhooks is reached )

Discord Proxy will map the HTTP response code from Discord to a gRPC status codes. In addition the details field will contain the full error information as JSON object.

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
    print(f"Code: {e.code()}")
    print(f"Details: {e.details()}")
```

> **Note**<br>For most cases it should be sufficient to deal with the status code. The JSON error code is only needed in some special cases.

## Timeouts

All requests are synchronous and sometimes it can take a few seconds for a request to complete due to Discord rate limiting. However, they might be issues with the network or the Discord API, which might case requests to go on for a long time. In order to build a robust application we recommend to use sensible timeouts with all requests. Note that this timeout must cover the complete duration it takes for a request to compete and should therefore not be set too short.

Here is how to use timeout with requests to the Discord Proxy. All timeouts are in seconds:

```Python
try:
    client.SendDirectMessage(request, timeout=10)
except grpc.RpcError as e:
    # handle timeouts
```

Should a timeout be triggered the client will receive a `grpc.RpcError` with status code `DEADLINE_EXCEEDED`.
