from fastmcp import FastMCP
from os import environ

from mcp_windows.media import mcp as media_mcp
from mcp_windows.notifications import mcp as notifications_mcp
from mcp_windows.window_management import mcp as window_management_mcp
from mcp_windows.monitors import mcp as monitors_mcp
from mcp_windows.clipboard import mcp as clipboard_mcp
from mcp_windows.screenshot import mcp as screenshot_mcp
from mcp_windows.theme import mcp as theme_mcp
from mcp_windows.startmenu import mcp as startmenu_mcp
from mcp_windows.keyboard import mcp as keyboard_mcp
from mcp_windows.audio import mcp as audio_mcp

sep = environ.get("FASTMCP_TOOL_SEPARATOR", "_")

mcp: FastMCP = FastMCP(
    name="windows",
)

mcp.mount("media", media_mcp, tool_separator=sep)
mcp.mount("notifications", notifications_mcp, tool_separator=sep)
mcp.mount("window_management", window_management_mcp, tool_separator=sep)
mcp.mount("monitors", monitors_mcp, tool_separator=sep)
mcp.mount("clipboard", clipboard_mcp, tool_separator=sep)
mcp.mount("screenshot", screenshot_mcp, tool_separator=sep)
mcp.mount("theme", theme_mcp, tool_separator=sep)
mcp.mount("startmenu", startmenu_mcp, tool_separator=sep)
mcp.mount("keyboard", keyboard_mcp, tool_separator=sep)
mcp.mount("audio", audio_mcp, tool_separator=sep)