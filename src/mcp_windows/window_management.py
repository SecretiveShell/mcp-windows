import asyncio
import json
import win32gui
import win32con
import win32process
import win32api
import psutil

from fastmcp import FastMCP

mcp: FastMCP = FastMCP(
    name="window_management"
)

def get_process_info(pid: int) -> dict:
    try:
        proc = psutil.Process(pid)
        return {
            "pid": pid,
            "exe": proc.name(),
        }
    except psutil.NoSuchProcess:
        return {
            "pid": pid,
            "exe": "<terminated>"
        }

@mcp.tool("get_foreground_window_info")
async def get_foreground_window_info() -> str:
    """Return information about the currently focused (foreground) window."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return json.dumps({"error": "No active window"})

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    info = get_process_info(pid)
    info.update({
        "hwnd": hwnd,
        "title": win32gui.GetWindowText(hwnd),
        "class": win32gui.GetClassName(hwnd),
    })
    return json.dumps(info, ensure_ascii=False)

@mcp.tool("get_window_list")
async def list_open_windows() -> str:
    """Return a list of all top-level visible windows."""
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            info = get_process_info(pid)
            info.update({
                "hwnd": hwnd,
                "title": win32gui.GetWindowText(hwnd),
                "class": win32gui.GetClassName(hwnd),
            })
            windows.append(info)

    win32gui.EnumWindows(callback, None)
    return json.dumps(windows, ensure_ascii=False)

@mcp.tool("focus_window")
async def focus_window(hwnd: int) -> str:
    """Force focus a window using all known safe tricks (thread attach, fake input, fallback restore)."""
    try:
        hwnd = int(hwnd)

        if not win32gui.IsWindow(hwnd):
            return "Invalid HWND"

        # Step 1: Only restore if minimized (prevent resizing)
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        # Step 2: Try normal focus via thread attach
        fg_hwnd = win32gui.GetForegroundWindow()
        fg_thread = win32process.GetWindowThreadProcessId(fg_hwnd)[0]
        current_thread = win32api.GetCurrentThreadId()

        if fg_thread != current_thread:
            win32process.AttachThreadInput(fg_thread, current_thread, True)

        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

        if fg_thread != current_thread:
            win32process.AttachThreadInput(fg_thread, current_thread, False)

        # Step 3: Check if it worked
        if win32gui.GetForegroundWindow() == hwnd:
            return "Focused window successfully"

        # Step 4: Fallback — simulate user input (to defeat foreground lock)
        win32api.keybd_event(0, 0, 0, 0)
        await asyncio.sleep(0.05)

        # Step 5: Try again
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

        if win32gui.GetForegroundWindow() == hwnd:
            return "Focused window (after simulating input)"

        # Step 6: Hard fallback — minimize + restore
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        await asyncio.sleep(0.2)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

        if win32gui.GetForegroundWindow() == hwnd:
            return "Focused window (after minimize/restore trick)"

        return "Could not focus window: OS restrictions"

    except Exception as e:
        return f"Could not focus window: {type(e).__name__}: {e}"


@mcp.tool("close_window")
async def close_window(hwnd: int) -> str:
    """Close the specified window."""
    try:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return "Closed window"
    except Exception as e:
        return f"Could not close window: {type(e).__name__}: {e}"

@mcp.tool("minimize_window")
async def minimize_window(hwnd: int) -> str:
    """Minimize the specified window."""
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        return "Minimized window"
    except Exception as e:
        return f"Could not minimize window: {type(e).__name__}: {e}"
