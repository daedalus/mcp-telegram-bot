# SPEC.md — mcp-telegram-bot

## Purpose
An MCP (Model Context Protocol) server that exposes a Telegram bot, allowing AI assistants to send messages, manage conversations, and interact with Telegram users through MCP tools and resources.

## Scope

### In Scope
- MCP server implementation using fastmcp
- Telegram Bot API integration via python-telegram-bot
- Tool for sending messages to Telegram chats
- Tool for getting bot information
- Tool for getting updates (recent messages)
- Resource for exposing bot status
- Support for stdio transport (MCP standard)

### Not Out of Scope
- Webhook support
- Inline keyboard/keyboard markup handling
- Media handling (photos, videos, files)
- Group/channel management
- User authentication/authorization
- Database persistence

## Public API / Interface

### MCP Tools

1. **`send_message`**
   - Signature: `send_message(chat_id: str, text: str) -> dict`
   - Sends a message to a specified Telegram chat
   - Returns: JSON response from Telegram API
   - Raises: ValueError if chat_id is invalid or text is empty

2. **`get_me`**
   - Signature: `get_me() -> dict`
   - Returns bot information (username, name, id, can_join_groups, etc.)

3. **`get_updates`**
   - Signature: `get_updates(limit: int = 10, offset: int | None = None) -> list[dict]`
   - Returns recent updates (messages, callbacks, etc.)
   - limit: Maximum number of updates to return (1-100)
   - offset: Identifier of the first returned update

### MCP Resources

1. **`bot://status`**
   - Returns bot status including: is_running, bot_info, last_update_time
   - Format: JSON

## Data Formats

### Environment Variables
- `TELEGRAM_BOT_TOKEN` (required): Telegram Bot API token from @BotFather

### API Response Format
- All Telegram API calls return JSON responses as documented in Telegram Bot API

## Edge Cases

1. **Empty bot token** - Raises error if TELEGRAM_BOT_TOKEN is not set
2. **Invalid bot token** - Telegram API returns 401 error, which is propagated
3. **Network failure** - Connection errors are raised as exceptions
4. **Empty message text** - send_message raises ValueError
5. **Invalid chat_id** - Telegram API returns error, which is propagated
6. **Rate limiting** - Telegram API returns 429, should be handled gracefully
7. **Invalid update offset** - Telegram API returns error
8. **Message send failure** - Exception with error details from Telegram API

## Performance & Constraints
- Single-threaded async operation
- No message queue (direct API calls)
- Maximum 100 updates per call
- Connection timeout: 30 seconds

