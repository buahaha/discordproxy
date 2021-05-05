# Operations Guide

## Installation

### Alliance Auth installation

This section describes how to install Discord Proxy into an existing Alliance Auth installation.

#### Install Discord Proxy

```eval_rst
.. note::
    This guide assumed a default installation according to the official Auth installation guide.
```

Login as root user, activate your venv and navigate to your Auth main folder:

```bash
cd /home/allianceserver/myauth
```

Install discordproxy from PyPI into the venv:

```bash
pip install discordproxy
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

```eval_rst
.. note::
    We do not recommend adding discordproxy to your myauth group, since it does not require to be restarted after myauth configuration changes like the other programs in that group.
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

Install discordproxy from PyPI into the venv:

```bash
pip install discordproxy
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
                          [--log-console-level {DEBUG,INFO,WARN,ERROR,CRITICAL}]
                          [--log-file-level {DEBUG,INFO,WARN,ERROR,CRITICAL}]
                          [--log-file-path LOG_FILE_PATH] [--version]

Server with HTTP API for sending messages to Discord

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Discord bot token. Can alternatively be specified as
                        environment variable DISCORD_BOT_TOKEN. (default:
                        None)
  --host HOST           server host address (default: 127.0.0.1)
  --port PORT           server port (default: 50051)
  --log-console-level {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        Log level of log file (default: CRITICAL)
  --log-file-level {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        Log level of log file (default: INFO)
  --log-file-path LOG_FILE_PATH
                        Path for storing the log file. If no path if provided,
                        the log file will be stored in the current working
                        folder (default: None)
  --version             show the program version and exit
```
