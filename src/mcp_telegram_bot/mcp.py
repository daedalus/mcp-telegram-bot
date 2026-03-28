import os
from datetime import datetime
from typing import Any

import fastmcp
from telegram import Bot
from telegram.error import TelegramError

mcp = fastmcp.FastMCP("mcp-telegram-bot")

_bot: Bot | None = None
_last_update_time: datetime | None = None


def get_bot() -> Bot:
    """Get or create Telegram bot instance."""
    global _bot
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
    if _bot is None:
        _bot = Bot(token=token)
    return _bot


@mcp.tool()
async def send_message(chat_id: str, text: str) -> dict[str, Any]:
    """Send a message to a specified Telegram chat.

    Args:
        chat_id: The Telegram chat ID to send the message to. Can be a numeric ID or username with @ prefix.
        text: The message text to send.

    Returns:
        JSON response from Telegram API containing message details.

    Raises:
        ValueError: If chat_id is invalid or text is empty.
        TelegramError: If Telegram API returns an error.
    """
    if not chat_id:
        raise ValueError("chat_id cannot be empty")
    if not text:
        raise ValueError("text cannot be empty")

    bot = get_bot()
    try:
        message = await bot.send_message(chat_id=chat_id, text=text)
        return message.to_dict()
    except TelegramError as e:
        raise RuntimeError(f"Telegram API error: {e.message}") from e


@mcp.tool()
async def get_me() -> dict[str, Any]:
    """Get bot information.

    Returns:
        JSON response containing bot information (id, username, first_name, etc.).
    """
    bot = get_bot()
    try:
        bot_info = await bot.get_me()
        return bot_info.to_dict()
    except TelegramError as e:
        raise RuntimeError(f"Telegram API error: {e.message}") from e


@mcp.tool()
async def get_updates(
    limit: int = 10, offset: int | None = None
) -> list[dict[str, Any]]:
    """Get recent updates from Telegram.

    Args:
        limit: Maximum number of updates to return (1-100). Defaults to 10.
        offset: Identifier of the first returned update. Only updates with id greater than offset are returned.

    Returns:
        List of update dictionaries from Telegram API.

    Raises:
        TelegramError: If Telegram API returns an error.
    """
    global _last_update_time

    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    bot = get_bot()
    try:
        updates = await bot.get_updates(limit=limit, offset=offset)
        _last_update_time = datetime.now()
        return [update.to_dict() for update in updates]
    except TelegramError as e:
        raise RuntimeError(f"Telegram API error: {e.message}") from e


@mcp.resource("bot://status")
async def bot_status() -> dict[str, Any]:
    """Get bot status including running state and information.

    Returns:
        JSON containing: is_running, bot_info, last_update_time
    """
    global _last_update_time

    bot_info = None
    try:
        bot_info = await get_me()
    except RuntimeError:
        pass

    return {
        "is_running": True,
        "bot_info": bot_info,
        "last_update_time": _last_update_time.isoformat()
        if _last_update_time
        else None,
    }
