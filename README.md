# mcp-telegram-bot

> MCP server that exposes a Telegram bot

[![PyPI](https://img.shields.io/pypi/v/mcp-telegram-bot.svg)](https://pypi.org/project/mcp-telegram-bot/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-telegram-bot.svg)](https://pypi.org/project/mcp-telegram-bot/)
[![Coverage](https://codecov.io/gh/daedalus/mcp-telegram-bot/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/mcp-telegram-bot)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install mcp-telegram-bot
```

## Setup

1. Create a Telegram bot by talking to @BotFather on Telegram
2. Get your bot token
3. Set the `TELEGRAM_BOT_TOKEN` environment variable

## Usage

```bash
export TELELEGRAM_BOT_TOKEN="your-bot-token-here"
mcp-telegram-bot
```

### MCP Tools

- **send_message**: Send a message to a Telegram chat
- **get_me**: Get bot information
- **get_updates**: Get recent updates from Telegram

### MCP Resources

- **bot://status**: Get bot status

mcp-name: io.github.daedalus/mcp-telegram-bot

## Development

```bash
git clone https://github.com/daedalus/mcp-telegram-bot.git
cd mcp-telegram-bot
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

## License

MIT
