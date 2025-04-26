# AI-MCP-NET-ANALYSIS

A Model Context Protocol (MCP) module for performing network analysis from a LLM chat client or an agent.

## Configuration

### Claude GPT client

- Add MCP configuration to ```~/Library/Application Support/Claude/claude_desktop_config.json```.
```json
{
  "mcpServers": {

    "AI-MCP-NET-ANALYSIS": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--init",
        "--network", "host",
        "--privileged",
        "--name", "ai-mcp-net-analysis-tmp",
        "ai-mcp-net-analysis"
      ]
    }
  }
}
```