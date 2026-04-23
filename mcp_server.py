from mcp.server.fastmcp import FastMCP
# import bludoor_mcp_claude_integration.tools.get_spent
import bludoor_mcp_claude_integration.tools.lightspeed_data
# Test with MCP Inspector [ uv run mcp dev mcp_server.py ]

mcp = FastMCP("BlueDoor assistant")

@mcp.prompt()
def assistant(user_name: str, user_title: str) -> str:
    """Global instructions for assistant"""
    with open("prompts/assistant.md", "r") as file:
        template = file.read()
    return template.format(user_name=user_name, user_title=user_title)

@mcp.resource("http://sample_response/spent")
def sample_response() -> str:
    with open("sample_response/spent.md", "r") as file:
        return file.read()

# @mcp.tool()
# def spent_tool(user_input: str) -> str:
#     """
#     EXTRACTION INSTRUCTION: Extract only the name from the user's query.

#     Examples:
#     "Get the row data for John Coding" -> user_input should be "John Coding"
#     """
#     return tools.get_spent.main(user_input)

@mcp.tool()
def lightspeed_tool(user_input: str) -> list:
    """
    EXTRACTION INSTRUCTION: Extract only the name from the user's query.

    Examples:
    "Get the Lightspeed row data for John Smith" -> user_input should be "John Smith"
#   "Get me all the current lightspeed data" -> user_input should be "*"
    "Get me the clients data that live in 10001 New York New York" -> user_input should be "location 10001 New York New York"
    "Search by area for the clients that live in 18015 Bethlehem PA" -> user_input should be "location 18015 Bethlehem PA"
    """
    return bludoor_mcp_claude_integration.tools.lightspeed_data.main(user_input)


if __name__ == "__main__":
    mcp.run(transport='stdio')