from fastmcp import FastMCP
import asyncio
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mcp: FastMCP = FastMCP(
    name="audio"
)

def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args))

@mcp.tool("get_volume")
async def get_volume() -> str:
    """Return the master volume level as a percentage (0-100)."""
    volume = await run_in_executor(_get_volume_interface)
    level = await run_in_executor(volume.GetMasterVolumeLevelScalar)
    return f"{int(level * 100)}"

@mcp.tool("set_volume")
async def set_volume(level: int) -> str:
    """Set the master volume level (0-100)."""
    if not 0 <= level <= 100:
        return "Volume must be between 0 and 100"
    volume = await run_in_executor(_get_volume_interface)
    await run_in_executor(volume.SetMasterVolumeLevelScalar, level / 100.0, None)
    return f"Volume set to {level}%"

@mcp.tool("mute")
async def mute() -> str:
    volume = await run_in_executor(_get_volume_interface)
    await run_in_executor(volume.SetMute, 1, None)
    return "Muted"

@mcp.tool("unmute")
async def unmute() -> str:
    volume = await run_in_executor(_get_volume_interface)
    await run_in_executor(volume.SetMute, 0, None)
    return "Unmuted"
