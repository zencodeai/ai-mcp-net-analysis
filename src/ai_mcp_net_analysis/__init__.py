from .server import serve


def main():
    """MCP network analysis - network analysis for MCP"""
    import asyncio

    asyncio.run(serve())


if __name__ == "__main__":
    main()
