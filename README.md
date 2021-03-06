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
