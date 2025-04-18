from fastmcp import FastMCP

from mcp_windows.media import mcp as media_mcp
from mcp_windows.notifications import mcp as notifications_mcp

mcp: FastMCP = FastMCP(
    name="windows",
)

mcp.mount("media", media_mcp, tool_separator=".")
mcp.mount("notifications", notifications_mcp, tool_separator=".")