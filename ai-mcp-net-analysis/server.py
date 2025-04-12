import os

# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP

from utils import ConfigParser, ConfigData
from utils import Logger, LoggerFactory


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


# Sample ping sweep return
PING_SWEEP_RESULT = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<?xml-stylesheet href="file:///opt/homebrew/bin/../share/nmap/nmap.xsl" type="text/xsl"?>
<!-- Nmap 7.95 scan initiated Wed Apr  9 20:31:28 2025 as: nmap -oX - -sn -PE 192.168.1.0/24 -->
<nmaprun scanner="nmap" args="nmap -oX - -sn -PE 192.168.1.0/24"
 start="1744245088"
 startstr="Wed Apr  9 20:31:28 2025"
 version="7.95"
 xmloutputversion="1.05">
<verbose level="0"/>
<debugging level="0"/>
<host><status state="up" reason="syn-ack" reason_ttl="0"/>
<address addr="192.168.1.1" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="4691" rttvar="5000" to="100000"/>
</host>
<host><status state="up" reason="conn-refused" reason_ttl="0"/>
<address addr="192.168.1.100" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="31995" rttvar="31995" to="159975"/>
</host>
<host><status state="up" reason="conn-refused" reason_ttl="0"/>
<address addr="192.168.1.105" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="6071" rttvar="6071" to="100000"/>
</host>
<host><status state="up" reason="conn-refused" reason_ttl="0"/>
<address addr="192.168.1.124" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="52086" rttvar="52086" to="260430"/>
</host>
<host><status state="up" reason="conn-refused" reason_ttl="0"/>
<address addr="192.168.1.125" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="4705" rttvar="5000" to="100000"/>
</host>
<host><status state="up" reason="conn-refused" reason_ttl="0"/>
<address addr="192.168.1.126" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="221" rttvar="5000" to="100000"/>
</host>
<host><status state="up" reason="conn-refused" reason_ttl="0"/>
<address addr="192.168.1.143" addrtype="ipv4"/>
<hostnames>
</hostnames>
<times srtt="7377" rttvar="7377" to="100000"/>
</host>
<runstats>
<finished
 time="1744245098"
 timestr="Wed Apr  9 20:31:38 2025"
 summary="Nmap done at Wed Apr  9 20:31:38 2025; 256 IP addresses (7 hosts up) scanned in 9.89 seconds"
 elapsed="9.89" exit="success"/><hosts up="7" down="249" total="256"/>
</runstats>
</nmaprun>
"""


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
    log.log_info(f"Starting ping sweep for {ip_cidr} with timeout {timeout_s} seconds.")
    return PING_SWEEP_RESULT
