# mcp-windows

MCP server for the windows API.

## Installation

add this to your claude mcp config:

```json
{
  "mcpServers": {
    "windows": {
      "command": "uvx",
      "args": [
        "mcp-windows"
      ]
    }
  }
}
```

or locally:

```json
{
  "mcpServers": {
    "windows": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\{name}\\Documents\\mcp-windows",
        "run",
        "mcp-windows"
      ]
    }
  }
}
```

## Features

### Media

- get_media_sessions
- pause
- play

### Notifications

- send_toast

### Window Management

- get_foreground_window_info
- get_window_list
- focus_window
- close_window
- minimize_window

### Monitors

- sleep_monitors
- wake_monitors

## License

MIT