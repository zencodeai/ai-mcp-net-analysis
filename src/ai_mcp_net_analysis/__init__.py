from .server_bak import serve


def main():
    """MCP network analysis - network analysis for MCP"""
    import asyncio

    asyncio.run(serve())


__all__ = ["main"]


if __name__ == "__main__":
    main()
