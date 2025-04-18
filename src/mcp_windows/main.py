from fastmcp import FastMCP

from mcp_windows.media import mcp as media_mcp

mcp: FastMCP = FastMCP(
    name="windows",
)

mcp.mount("media", media_mcp, tool_separator=".")

