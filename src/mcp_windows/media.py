import json

from fastmcp import FastMCP
from winrt.windows.foundation import IAsyncOperation
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionMediaProperties as MediaProperties,
    GlobalSystemMediaTransportControlsSessionPlaybackInfo as PlaybackInfo,
)

mcp: FastMCP = FastMCP(
    name="Media",
)

PLAYBACK_STATUS = {
    0: "closed",
    1: "opened",
    2: "changing",
    3: "stopped",
    4: "playing",
    5: "paused",
}


@mcp.tool("get_media_sessions")
async def get_media_sessions() -> str:
    """List all media playback sessions with metadata and control capability info."""

    manager_op: IAsyncOperation = MediaManager.request_async()
    manager = await manager_op
    sessions = manager.get_sessions()

    output = {}
    for session in sessions:
        props_op = session.try_get_media_properties_async()
        props: MediaProperties = await props_op
        playback_info: PlaybackInfo = session.get_playback_info()
        controls = playback_info.controls

        app_id = session.source_app_user_model_id

        output[app_id] = {
            "title": props.title or "unknown",
            "artist": props.artist or "unknown",
            "album_title": props.album_title or "unknown",
            "playback_status": str(PLAYBACK_STATUS.get(playback_info.playback_status)),
            "is_play_enabled": controls.is_play_enabled,
            "is_pause_enabled": controls.is_pause_enabled,
            "is_next_enabled": controls.is_next_enabled,
            "is_previous_enabled": controls.is_previous_enabled,
        }

    return json.dumps(output)


@mcp.tool("pause")
async def pause(app_id: str) -> str:
    """Pause the media playback for a given app_id using windows media control API."""

    manager_op: IAsyncOperation[MediaManager] = MediaManager.request_async()
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

    manager_op: IAsyncOperation[MediaManager] = MediaManager.request_async()
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


@mcp.tool("next")
async def next(app_id: str) -> str:
    """Skip to the next media item for the given app_id."""

    manager = await MediaManager.request_async()
    sessions = manager.get_sessions()

    for session in sessions:
        if session.source_app_user_model_id.lower() == app_id.lower():
            playback_info = session.get_playback_info()
            if playback_info.controls.is_next_enabled:
                await session.try_skip_next_async()
                return "Skipped to next track"
            else:
                return "Next track not available"

    return "Session not found"


@mcp.tool("previous")
async def previous(app_id: str) -> str:
    """Skip to the previous media item for the given app_id."""

    manager = await MediaManager.request_async()
    sessions = manager.get_sessions()

    for session in sessions:
        if session.source_app_user_model_id.lower() == app_id.lower():
            playback_info = session.get_playback_info()
            if playback_info.controls.is_previous_enabled:
                await session.try_skip_previous_async()
                return "Skipped to previous track"
            else:
                return "Previous track not available"

    return "Session not found"
