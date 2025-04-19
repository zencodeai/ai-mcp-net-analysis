from abc import ABC, abstractmethod

from mcp.types import Tool as MCPTool


class ToolError(Exception):
    """
    Custom exception class for tool-related errors.
    """
    pass


class Tool(ABC):
    """
    An abstract class representing a tool with a name, description, and function.
    """

    # Tools registry
    _tools = {}

    @classmethod
    def register_tool(cls, tool_name: str, tool: "Tool") -> None:
        """
        Register a tool with the given name and metadata.
        """
        cls._tools[tool_name] = tool

    @classmethod
    def exec_tool(cls, tool_name: str, arguments: dict) -> any:
        """
        Execute a registered tool with the given name and arguments.
        """
        if tool_name not in cls._tools:
            raise ToolError(f"Tool '{tool_name}' not found.")
        tool = cls._tools[tool_name]
        return tool.exec(arguments)

    @abstractmethod
    def get_tool(self) -> MCPTool:
        """
        Abstract method to be implemented by subclasses.
        This method should return the tool's metadata.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Abstract method to be implemented by subclasses.
        This method should return the tool's name.
        """
        pass

    @abstractmethod
    def exec(self, arguments: dict) -> any:
        """
        Abstract method to be implemented by subclasses.
        This method should contain the logic for the tool's functionality.
        """
        pass
