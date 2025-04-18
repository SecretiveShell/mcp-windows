import win32clipboard
import win32con
from fastmcp import FastMCP


mcp: FastMCP = FastMCP(
    name="clipboard",
)

@mcp.tool("get_clipboard")
async def get_clipboard() -> str:
    """Get the current clipboard contents."""
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return data

@mcp.tool("set_clipboard")
async def set_clipboard(text: str) -> str:
    """Set the clipboard contents."""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return "Clipboard set"
