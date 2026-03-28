import os
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_env_bot_token() -> Generator[None, None, None]:
    """Set TELEGRAM_BOT_TOKEN in environment."""
    with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test_token_123"}):
        yield


@pytest.fixture
def mock_bot() -> Generator[AsyncMock, None, None]:
    """Create a mock Telegram Bot."""
    with patch("mcp_telegram_bot.mcp.get_bot") as mock_get_bot:
        bot = AsyncMock()
        mock_get_bot.return_value = bot
        yield bot


@pytest.fixture
def reset_bot() -> Generator[None, None, None]:
    """Reset the global _bot variable between tests."""
    import mcp_telegram_bot.mcp as mcp_module

    mcp_module._bot = None
    mcp_module._last_update_time = None
    yield
    mcp_module._bot = None
    mcp_module._last_update_time = None
