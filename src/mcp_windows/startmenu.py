from fastmcp import FastMCP
import os
from winrt.windows.foundation import Uri
from winrt.windows.system import Launcher
from winrt.windows.storage import StorageFile

mcp: FastMCP = FastMCP(
    name="startmenu",
)

@mcp.tool("open_file")
async def open_file(path: str) -> str:
    """Open a file or folder in the default application."""
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return f"Path does not exist: {path}"
    
    file = await StorageFile.get_file_from_path_async(path)
    success = await Launcher.launch_file_async(file)

    if success:
        return "Opened file"

    # Fallback to os.startfile if the above fails
    os.startfile(path)
    return "Opened file"

@mcp.tool("open_url")
async def open_url(url: str) -> str:
    """Open a URL in the default browser."""
    try:
        uri = Uri(url)
        success = await Launcher.launch_uri_async(uri)
        if success:
            return "Opened URL"
    except Exception:
        pass
    
    # Fallback to webbrowser if the above fails
    import webbrowser
    webbrowser.open(url)
    return "Opened URL"