from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from telegram.error import TelegramError


@pytest.mark.asyncio
async def test_send_message_success(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test sending a message successfully."""
    from mcp_telegram_bot.mcp import send_message

    mock_message = MagicMock()
    mock_message.to_dict.return_value = {
        "message_id": 123,
        "chat": {"id": 456, "type": "private"},
        "text": "Hello world",
    }
    mock_bot.send_message.return_value = mock_message

    result = await send_message(chat_id="456", text="Hello world")

    assert result["message_id"] == 123
    assert result["text"] == "Hello world"
    mock_bot.send_message.assert_called_once_with(chat_id="456", text="Hello world")


@pytest.mark.asyncio
async def test_send_message_empty_chat_id() -> None:
    """Test send_message raises ValueError for empty chat_id."""
    from mcp_telegram_bot.mcp import send_message

    with pytest.raises(ValueError, match="chat_id cannot be empty"):
        await send_message(chat_id="", text="Hello")


@pytest.mark.asyncio
async def test_send_message_empty_text() -> None:
    """Test send_message raises ValueError for empty text."""
    from mcp_telegram_bot.mcp import send_message

    with pytest.raises(ValueError, match="text cannot be empty"):
        await send_message(chat_id="456", text="")


@pytest.mark.asyncio
async def test_send_message_api_error(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test send_message raises RuntimeError on Telegram API error."""
    from mcp_telegram_bot.mcp import send_message

    mock_bot.send_message.side_effect = TelegramError("Chat not found")

    with pytest.raises(RuntimeError, match="Telegram API error: Chat not found"):
        await send_message(chat_id="999", text="Hello")


@pytest.mark.asyncio
async def test_get_me_success(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test getting bot information successfully."""
    from mcp_telegram_bot.mcp import get_me

    mock_user = MagicMock()
    mock_user.to_dict.return_value = {
        "id": 123456,
        "is_bot": True,
        "username": "test_bot",
        "first_name": "Test Bot",
    }
    mock_bot.get_me.return_value = mock_user

    result = await get_me()

    assert result["id"] == 123456
    assert result["username"] == "test_bot"
    assert result["first_name"] == "Test Bot"


@pytest.mark.asyncio
async def test_get_updates_success(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test getting updates successfully."""
    from mcp_telegram_bot.mcp import get_updates

    mock_update = MagicMock()
    mock_update.to_dict.return_value = {
        "update_id": 123,
        "message": {"message_id": 1, "text": "Hello"},
    }
    mock_bot.get_updates.return_value = [mock_update]

    result = await get_updates(limit=10)

    assert len(result) == 1
    assert result[0]["update_id"] == 123


@pytest.mark.asyncio
async def test_get_updates_invalid_limit() -> None:
    """Test get_updates raises ValueError for invalid limit."""
    from mcp_telegram_bot.mcp import get_updates

    with pytest.raises(ValueError, match="limit must be between 1 and 100"):
        await get_updates(limit=0)


@pytest.mark.asyncio
async def test_get_updates_api_error(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test get_updates raises RuntimeError on Telegram API error."""
    from mcp_telegram_bot.mcp import get_updates

    mock_bot.get_updates.side_effect = TelegramError("Bad Request")

    with pytest.raises(RuntimeError, match="Telegram API error: Bad Request"):
        await get_updates()


@pytest.mark.asyncio
async def test_bot_status_running(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test bot_status resource returns running status."""
    from mcp_telegram_bot.mcp import bot_status

    mock_user = MagicMock()
    mock_user.to_dict.return_value = {
        "id": 123456,
        "username": "test_bot",
    }
    mock_bot.get_me.return_value = mock_user

    result = await bot_status()

    assert result["is_running"] is True
    assert result["bot_info"]["id"] == 123456


def test_get_bot_no_token(reset_bot: Generator[None, None, None]) -> None:
    """Test get_bot raises ValueError when token is not set."""
    import os

    from mcp_telegram_bot.mcp import get_bot

    env = os.environ.copy()
    os.environ.pop("TELEGRAM_BOT_TOKEN", None)

    with pytest.raises(
        ValueError, match="TELEGRAM_BOT_TOKEN environment variable is not set"
    ):
        get_bot()

    os.environ.update(env)


@pytest.mark.asyncio
async def test_get_updates_with_offset(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test get_updates with offset parameter."""
    from mcp_telegram_bot.mcp import get_updates

    mock_update = MagicMock()
    mock_update.to_dict.return_value = {"update_id": 200}
    mock_bot.get_updates.return_value = [mock_update]

    result = await get_updates(limit=5, offset=100)

    assert len(result) == 1
    mock_bot.get_updates.assert_called_once_with(limit=5, offset=100)


@pytest.mark.asyncio
async def test_bot_status_no_bot_info(
    mock_env_bot_token: Generator[None, None, None],
    mock_bot: AsyncMock,
    reset_bot: Generator[None, None, None],
) -> None:
    """Test bot_status when bot info is unavailable."""
    from mcp_telegram_bot.mcp import bot_status

    mock_bot.get_me.side_effect = RuntimeError("Network error")

    result = await bot_status()

    assert result["is_running"] is True
    assert result["bot_info"] is None
