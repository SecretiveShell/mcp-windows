import json
from fastmcp import FastMCP
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager, GlobalSystemMediaTransportControlsSessionMediaProperties as MediaProperties
from winrt.windows.foundation import IAsyncOperation

mcp: FastMCP = FastMCP(
    name="Media",
)

@mcp.tool("get_media_sessions")
async def get_media_sessions() -> str:
    """List all media playback sessions using windows media control API."""

    manager_op: IAsyncOperation = MediaManager.request_async()
    manager = await manager_op
    sessions = manager.get_sessions()

    output = {}
    for session in sessions:
        props_op = session.try_get_media_properties_async()
        props: MediaProperties = await props_op
        app_id = session.source_app_user_model_id

        output[app_id] = {
            "title": props.title or "unknown",
            "artist": props.artist or "unknown",
            "album_title": props.album_title or "unknown",
        }
    
    return json.dumps(output)

@mcp.tool("pause")
async def pause(app_id: str) -> str:
    """Pause the media playback for a given app_id using windows media control API."""

    manager_op: IAsyncOperation[MediaManager] = \
    MediaManager.request_async()
    manager: MediaManager = await manager_op

    sessions = manager.get_sessions()
    for session in sessions:
        if session.source_app_user_model_id.lower() == app_id.lower():
            playback_info = session.get_playback_info()
            if playback_info.controls.is_pause_enabled:
                await session.try_pause_async()
                return "Paused"
            else:
                return "Pause not available"
            
    return "Session not found"

@mcp.tool("play")
async def play(app_id: str) -> str:
    """Play the media playback for a given app_id using windows media control API."""

    manager_op: IAsyncOperation[MediaManager] = \
    MediaManager.request_async()
    manager: MediaManager = await manager_op

    sessions = manager.get_sessions()
    for session in sessions:
        if session.source_app_user_model_id.lower() == app_id.lower():
            playback_info = session.get_playback_info()
            if playback_info.controls.is_play_enabled:
                await session.try_play_async()
                return "Playing"
            else:
                return "Play not available"
            
    return "Session not found"