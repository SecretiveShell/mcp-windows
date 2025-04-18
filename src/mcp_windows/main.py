from fastmcp import FastMCP
from os import environ

from mcp_windows.media import mcp as media_mcp
from mcp_windows.notifications import mcp as notifications_mcp
from mcp_windows.window_management import mcp as window_management_mcp

sep = environ.get("FASTMCP_TOOL_SEPARATOR", "_")

mcp: FastMCP = FastMCP(
    name="windows",
)

mcp.mount("media", media_mcp, tool_separator=sep)
mcp.mount("notifications", notifications_mcp, tool_separator=sep)
mcp.mount("window_management", window_management_mcp, tool_separator=sep)
