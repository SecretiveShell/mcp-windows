import win32api
import win32con
import asyncio
from fastmcp import FastMCP

mcp: FastMCP = FastMCP(
    name="keyboard",
)

@mcp.tool("type_text")
async def type_text(text: str, delay: float = 0.05):
    """Simulate typing text with a delay between each character. ONLY USE THIS AS A LAST RESORT."""
    for char in text:
        vk = ord(char.upper())
        needs_shift = char.isupper() or not char.isalnum()  # crude shift detection

        if needs_shift:
            win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)

        win32api.keybd_event(vk, 0, 0, 0)
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)

        if needs_shift:
            win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)

        await asyncio.sleep(delay)


VK_LOOKUP = {
    'ctrl': win32con.VK_CONTROL,
    'shift': win32con.VK_SHIFT,
    'alt': win32con.VK_MENU,
    'esc': win32con.VK_ESCAPE,
    'enter': win32con.VK_RETURN,
    'tab': win32con.VK_TAB,
    'space': win32con.VK_SPACE,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT,
    'up': win32con.VK_UP,
    'down': win32con.VK_DOWN,
}

@mcp.tool("send_keyboard_shortcut")
async def press_keys(keys: list[str]):
    """Simulate pressing a combination of keys. Use any of the following special keys: ctrl, shift, alt, esc, enter, tab, space, left, right, up, down as well the regular characters. ONLY USE THIS AS A LAST RESORT."""
    vk_keys = []
    for k in keys:
        k_lower = k.lower()
        vk = VK_LOOKUP.get(k_lower, ord(k.upper()))
        vk_keys.append(vk)

    for vk in vk_keys:
        win32api.keybd_event(vk, 0, 0, 0)
    await asyncio.sleep(0.05)
    for vk in reversed(vk_keys):
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
