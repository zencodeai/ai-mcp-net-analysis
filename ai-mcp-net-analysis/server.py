import os

# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP

from utils import ConfigParser, ConfigData
from utils import Logger, LoggerFactory

from tools import ToolsNetDiscovery


@dataclass
class AppContext:
    """Application context"""
    config: ConfigData
    logger: Logger


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # The config path from the CONFIG_PATH environment variable
    # or default to "config/config.yaml"
    cfg_path = os.getenv("MCP_NET_ANALYSIS_CONFIG_PATH", "config/config.yaml")
    config: ConfigParser = ConfigParser.get_config(cfg_path)

    # Initialize the logger
    config_data = config.config
    logger: Logger = LoggerFactory.get_logger(config_data)

    try:
        logger.log_info("Starting the application.")
        yield AppContext(config=config_data, logger=logger)
    finally:
        # Cleanup on shutdown
        logger: Logger = LoggerFactory.get_logger()
        logger.log_info("Shutting down the application.")


# MCP server and config data
mcp: FastMCP = FastMCP("AI-MCP-NET-ANALYSIS", lifespan=app_lifespan)


# Process execution
def process_exception(e: Exception, ctx: Context) -> str:
    """Handle exceptions during process execution"""
    # Get logger instance
    log: Logger = ctx.request_context.lifespan_context.logger

    # Log the entire exception stack trace if level is debug
    log.log_debug(f"Exception: {e}")
    log.log_debug(f"Traceback: {e.__traceback__}")

    # Convert the excetpion to a detilled xml format
    # with type, attributes and message and return it
    return f"<error type='{type(e).__name__}' message='{str(e)}'>"


# Access type-safe lifespan context in tools
@mcp.tool()
def nmap_ping_sweep(ip_cidr: str, timeout_s: int, ctx: Context) -> str:
    """
    Perform a ping sweep of a network using nmap.
    Return the result in XML format.
    :param ip_cidr: CIDR notation for the IP range to scan.
    :param timeout_s: Timeout in seconds for the scan. 60 seconds is the default.
    """

    # Get logger instance
    log: Logger = ctx.request_context.lifespan_context.logger

    # Execute tool
    try:
        log.log_info("Executing nmap ping sweep.")
        log.log_debug(f"For {ip_cidr} with timeout {timeout_s} seconds.")
        result = ToolsNetDiscovery.nmap_ping_sweep(ip_cidr, timeout_s)
        log.log_debug(f"nmap ping sweep executed successfully:\n{result}")
        return result
    except Exception as e:
        return process_exception(e, ctx)


# Run the server
if __name__ == "__main__":
    # Start the server
    mcp.run()
