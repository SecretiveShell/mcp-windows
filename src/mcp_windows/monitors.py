import ctypes
import win32con
import win32gui

from fastmcp import FastMCP

mcp: FastMCP = FastMCP(
    name="monitors",
)

@mcp.tool("sleep_monitors")
async def sleep_monitors() -> str:
    """Put all monitors to sleep."""
    try:
        ctypes.windll.user32.SendMessageW(
            win32con.HWND_BROADCAST,
            win32con.WM_SYSCOMMAND,
            win32con.SC_MONITORPOWER,
            2  # 2 = power off
        )
        return "Monitors put to sleep"
    except Exception as e:
        return f"Failed to sleep monitors: {type(e).__name__}: {e}"

@mcp.tool("wake_monitors")
async def wake_monitors() -> str:
    """Wake up sleeping monitors."""
    try:
        # This is dumb, but moving the mouse 1px wakes monitors
        x, y = win32gui.GetCursorPos()
        ctypes.windll.user32.SetCursorPos(x, y + 1)
        ctypes.windll.user32.SetCursorPos(x, y)
        return "Monitors woken up"
    except Exception as e:
        return f"Failed to wake monitors: {type(e).__name__}: {e}"
