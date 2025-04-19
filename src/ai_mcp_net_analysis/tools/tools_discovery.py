from dataclasses import dataclass

from utils import CmdExec, CIDRIPContainer, TimeoutSecContainer
from tools.tool import Tool

from mcp.types import Tool as MCPTool


class ToolPingSweep(Tool):
    """
    Network host discovery class.
    This class is responsible for discovering network hosts and their statuses.
    """

    # Dataclass for function arguments
    @dataclass
    class Arguments:
        """
        Arguments for the ping sweep function.
        """
        ip_cidr: str
        timeout_s: int

        def __init__(self, args: dict):
            """
            Initialize the Arguments dataclass with the provided arguments.
            :param args: Dictionary containing the arguments.
            """
            self.ip_cidr = args.get("ip_cidr")
            self.timeout_s = args.get("timeout_s")

    def __init__(self):
        """
        Initialize the ToolPingSweep class.
        """
        super().__init__()
        # Register the tool with the class nam
        Tool.register_tool(self.__class__.__name__, self)

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

    def exec(self, arguments: dict) -> any:
        """
        Invokes the tool with the provided arguments.
        """
        # Create an instance of the Arguments dataclass
        args = self.Arguments(arguments)

        # Call the ping_sweep method with the arguments
        return self.ping_sweep(args)

    def ping_sweep(self, args: Arguments) -> str:
        """
        Perform a ping sweep of a network using nmap.
        :param args: Arguments containing the CIDR IP address and timeout.
        :return: The XML output from nmap.
        """
        # Validate the CIDR IP address
        cidr = CIDRIPContainer(args.ip_cidr)

        # Validate the timeout
        timeout = TimeoutSecContainer(args.timeout_s)

        # Execute the command and capture the output
        command = ["nmap", "-oX", "-", "-sn", "-PE", "--max-retries", "0", "--host-timeout", f"{timeout}s", f"{cidr}"]
        result = CmdExec.execute(command)
        return result
