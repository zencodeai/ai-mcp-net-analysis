from typing import Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

from utils import ConfigParser
from utils import Logger, LoggerFactory
from tools import Tool as ServerTool


async def serve() -> None:

    # Load the configuration
    cfg_path = "config/config.yaml"
    config = ConfigParser.get_config(cfg_path)

    # Intnialize the logger
    config_data = config.config
    logger: Logger = LoggerFactory.get_logger(config_data)

    # Create server instance
    logger.log_info("Creating server instance...")
    server = Server(config_data.mcp.name)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools' metadata."""
        logger.log_info("Listing tools...")
        return ServerTool.get_tools()

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """ Handle tools calls. """
        logger.log_info(f"Calling tool: {name} with arguments: {arguments}")
        result: str = ServerTool.exec_tool(name, arguments)
        return [TextContent(type="text", text=result)]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
