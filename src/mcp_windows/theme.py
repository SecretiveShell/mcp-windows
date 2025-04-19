from typing import Literal
import winreg
from fastmcp import FastMCP

mcp: FastMCP = FastMCP(
    name="theme",
)


def _set_theme_key(name: str, value: int):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)

@mcp.tool("set_theme_mode")
async def set_theme_mode(mode: Literal["dark", "light"]) -> str:
    """Set Windows UI theme to 'dark' or 'light'."""

    if mode.lower() not in {"dark", "light"}:
        return "Invalid mode. Use 'dark' or 'light'."

    val = 0 if mode == "dark" else 1
    try:
        _set_theme_key("AppsUseLightTheme", val)
        _set_theme_key("SystemUsesLightTheme", val)
        return f"Set theme to {mode}"
    except Exception as e:
        return f"Failed to set theme: {type(e).__name__}: {e}"


@mcp.tool("get_theme_mode")
async def get_theme_mode() -> str:
    """Get the current Windows UI theme."""

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if val else "dark"
    except Exception:
        return "unknown"
