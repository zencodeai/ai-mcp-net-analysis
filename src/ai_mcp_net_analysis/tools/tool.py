from abc import ABC, abstractmethod
from typing import Any

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
    def register_tool(cls, tool: "Tool") -> None:
        """
        Register a tool with the given name and metadata.
        """
        # Add tool to cls._tools dictionary if it is not already present else ignore
        name: str = tool.get_name()
        if name not in cls._tools:
            cls._tools[name] = tool
        else:
            raise ToolError(f"Tool '{name}' is already registered.")

    @classmethod
    def register_tools(cls) -> None:
        """
        Instantiate and register all tools if not already done.
        """
        # Check if tools are already registered
        if cls._tools:
            return

        # Register all subclasses of Tool
        for subclass in cls.__subclasses__():
            tool_instance = subclass()
            cls.register_tool(tool_instance)

    @classmethod
    def get_tools(cls) -> list[MCPTool]:
        """
        Get a list of all registered tools.
        """
        cls.register_tools()
        return [tool.get_tool() for tool in cls._tools.values()]

    @classmethod
    def exec_tool(cls, tool_name: str, arguments: dict) -> Any:
        """
        Execute a registered tool with the given name and arguments.
        """
        cls.register_tools()
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
    def exec(self, arguments: dict) -> Any:
        """
        Abstract method to be implemented by subclasses.
        This method should contain the logic for the tool's functionality.
        """
        pass
