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

- [Overview](#overview)
- [Installation](#installation)
- [Server configuration](#server-configuration)
- [Developer Guide](#developer-guide)
- [FAQ](#faq)
- [Change Log](CHANGELOG.md)

## Overview

**Discord Proxy** is a proxy server that provides access to the Discord API via gRPC.

The main purpose is to enable applications to use the Discord API without having to implement Discord's websocket protocol. Instead, applications can use the gRPC API and the proxy will resolve all requests with the Discord API server via websockets or HTTP.

Python applications can import the generated gRPC client directly. Applications in other languages can use the protobuf definition to generate their own gRPC client.

## Installation

### Alliance Auth installation

This section describes how to install Discord Proxy into an existing Alliance Auth installation.

#### Install Discord Proxy

> **Note**<br>This guide assumed a default installation according to the official Auth installation guide.

Login as root user, activate your venv and navigate to your Auth main folder:

```bash
cd /home/allianceserver/myauth
```

Install discordproxy from the repo into the venv:

```bash
pip install git+https://gitlab.com/ErikKalkoken/discordproxy.git
```

Add Discord Proxy to your supervisor configuration for Auth.

Edit supervisor.conf in your current folder and add the below section. Make sure to replace `YOUR-BOT-TOKEN` with your current Discord bot token:

```ini
[program:discordproxy]
command=/home/allianceserver/venv/auth/bin/discordproxyserver --token "YOUR-BOT-TOKEN"
directory=/home/allianceserver/myauth/log
user=allianceserver
numprocs=1
autostart=true
autorestart=true
stopwaitsecs=120
stdout_logfile=/home/allianceserver/myauth/log/discordproxyserver.out
stderr_logfile=/home/allianceserver/myauth/log/discordproxyserver.err
```

Add discordproxy to the myauth group:

```ini
[group:myauth]
programs=beat,worker,gunicorn,discordproxy
```

Reload supervisor to activate the changes and start Discord Proxy:

```bash
supervisorctl reload
```

To verify Discord Proxy is up and running you can check it's status:

```bash
supervisorctl status discordproxy
```

It should say "RUNNING".

### Stand-alone installation

This section describes how to install Discord Proxy as standalone server.

#### Create a Discord bot account

Follow [this guide](https://discordpy.readthedocs.io/en/latest/discord.html) to create your Discord bot:

1. Create a Discord application for your bot
2. Invite your bot to your Discord server

#### Install discordproxy on your server

Create a service user and switch to that user:

```bash
sudo adduser --disabled-login discordproxy
sudo su discordproxy
```

Setup a virtual environment for the server, activate it and update key packages:

```bash
cd /home/discordproxy
python3 -m venv venv
source venv/bin/activate
```

Update and install basic packages:

```bash
pip install -U pip
pip install wheel setuptools
```

Install discordproxy from the repo into the venv:

```bash
pip install git+https://gitlab.com/ErikKalkoken/discordproxy.git
```

#### Add discordproxy to supervisor

Create a supervisor configuration file - `/home/discordproxy/discordproxyserver.conf` - with the below template:

```ini
[program:discordproxy]
command=/home/discordproxy/venv/bin/discordproxyserver --token "YOUR-BOT-TOKEN"
directory=/home/discordproxy
user=discordproxy
numprocs=1
autostart=true
autorestart=true
stopwaitsecs=120
stdout_logfile=/home/discordproxy/discordproxyserver.out
stderr_logfile=/home/discordproxy/discordproxyserver.err
```

Add discordproxy to your supervisor configuration and restart supervisor to activate the change:

```bash
ln -s /home/discordproxy/discordproxyserver.conf /etc/supervisor/conf.d
supervisorctl reload
```

## Server configuration

Discord Proxy is designed to run via [supervisor](https://pypi.org/project/supervisor/) and can be configured with the below arguments. It comes with sensible defaults and will in most cases only need the Discord bot token to operate.

To configure your server just add/modify one of the below parameters in the respective command line of your supervisor configuration:

```text
usage: discordproxyserver [-h] [--token TOKEN] [--host HOST] [--port PORT]
                          [--log-level {INFO,WARN,ERROR,CRITICAL}]
                          [--log-file-path LOG_FILE_PATH] [--version]

Server with HTTP API for sending messages to Discord

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Discord bot token. Can alternatively be specified as
                        environment variable DISCORD_BOT_TOKEN. (default:
                        None)
  --host HOST           server host address (default: 127.0.0.1)
  --port PORT           server port (default: 50051)
  --log-level {INFO,WARN,ERROR,CRITICAL}
                        Log level of log file (default: INFO)
  --log-file-path LOG_FILE_PATH
                        Path for storing the log file. If no path if provided,
                        the log file will be stored in the current working
                        folder (default: None)
  --version             show the program version and exit
```

### Developer Guide

### Example

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

### Error handling

If a gRPC request fails a `grpc.RpcError` exception will be raised. RPC errors return the context of the request, consists of two fields:

- `code`: the [gRPC status code](https://grpc.github.io/grpc/core/md_doc_statuscodes.html)
- `details`: a string with additional details about the error.

The [Discord API](https://discord.com/developers/docs/topics/opcodes-and-status-codes) will return two types of error codes:

- HTTP response code (e.g. 404 if a request user does not exist)
- JSON error code (e.g. 30007 when the maximum number of webhooks is reached )

We have mapped the HTTP response code to gRPC status codes. In addition the details field will contain the full information as JSON object.

#### gRPC status codes

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

#### gRPC details

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

#### Example

Here is an example on how to get details for errors from your gRPC calls:

```python
try:
    client.SendDirectMessage(request)
except grpc.RpcError as e:
    print(e.args[0].code)
    print(e.args[0].details)
```

> **Note**<br>While this example only looks at the first element, `e.args` might actually contain more than one error.
