from typing import Any
from pydantic import BaseModel, field_validator

from utils import CmdExec
from utils import CIDRIPContainer
from utils import TimeoutSecContainer
from tools.tool import Tool

from mcp.types import Tool as MCPTool


class ToolPingSweep(Tool):
    """
    Network host discovery class.
    This class is responsible for discovering network hosts and their statuses.
    """

    # Dataclass for function arguments
    class Arguments(BaseModel):
        """
        Arguments for the ping sweep function.
        """
        ip_cidr: str
        timeout_s: int

        @field_validator("ip_cidr")
        def validate_ip_cidr(cls, value: str) -> str:
            """ Validate the CIDR IP address """
            _ = CIDRIPContainer(value)
            return value

        @field_validator("timeout_s")
        def validate_timeout_s(cls, value: int) -> int:
            """ Validate the timeout in seconds """
            _ = TimeoutSecContainer(value)
            return value

    def __init__(self):
        """
        Initialize the ToolPingSweep class.
        """
        super().__init__()

    def get_tool(self) -> MCPTool:
        """
        Returns the tool's metadata.
        """
        return MCPTool(
            name=self.get_name(),
            description="Perform a ping sweep on the specified network using nmap.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip_cidr": {
                        "type": "string",
                        "description": "CIDR notation of the IP range to scan (e.g., 192.168.0.0/24)."
                    },
                    "timeout_s": {
                        "type": "integer",
                        "description": "Timeout for each ping in seconds (e.g., 10). Default is 60 if not specified."
                    },
                },
                "required": ["ip_cidr", "timeout_s"],
            }
        )

    def get_name(self) -> str:
        """
        Get the tool's name.
        """
        return self.__class__.__name__

    def exec(self, arguments: dict) -> Any:
        """
        Invokes the tool with the provided arguments.
        """
        # Create an instance of the Arguments dataclass
        args = self.Arguments(
            ip_cidr=arguments.get("ip_cidr"),
            timeout_s=arguments.get("timeout_s")
        )

        # Call the ping_sweep method with the arguments
        return self.ping_sweep(args)

    def ping_sweep(self, args: Arguments) -> str:
        """
        Perform a ping sweep of a network using nmap.
        :param args: Arguments containing the CIDR IP address and timeout.
        :return: The XML output from nmap.
        """

        # Execute the command and capture the output
        command = [
            "nmap",
            "-oX",
            "-",
            "-sn",
            "-PE",
            "--max-retries", "0",
            "--host-timeout", f"{args.timeout_s}s",
            f"{args.ip_cidr}"]
        result = CmdExec.execute(command)
        return result
