**Claude MCP integration**

**Implemented**:

\- Connected Lightspeed

\- Return all data from Lightspeed

\- Search by name for Lightspeed

\- Search by zip code city and state for Lightspeed(requires all 3)

**To Do:**

\- implement search by zip code, city and state(individual/independent)

\- connect more systems(e.g. Kangaroo)

**Note:**

\- Environment variables are git ignored for security purposes. Requires a .env file in tools folder with proper API keys for routes

**How to run**

\- Make sure your mcp_server.py is ready and has your tools/prompts defined. Install dependencies

\-Claude Desktop reads MCP server configs from a JSON file. Open or create it:

\- macOS:
\- ~/Library/Application Support/Claude/claude_desktop_config.json
\- Windows:
\- %APPDATA%\Claude\claude_desktop_config.json

- Add your server to the config like this:

```json
    {
      "mcpServers": {
        "my-server": {
          "command": "python",
          "args": ["/absolute/path/to/mcp_server.py"]
        }
      }
    }
```

- Restart Claude Desktop

\- Go to File → Settings → Developer. You should see your server listed with a blue "running" status
\- Common issues: incorrect file paths, first run the code locally in an IDE(VSCode) to see if it errors, Check Claude's MCP logs(button in the same tab as the configuration file)

\- Test it: Open a new chat in Claude Desktop and try one of the sample prompts from the comments in mcp_server.py
