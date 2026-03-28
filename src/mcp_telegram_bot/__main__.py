from mcp_telegram_bot import mcp


def main() -> int:
    """Main entry point for the MCP Telegram Bot server."""
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
