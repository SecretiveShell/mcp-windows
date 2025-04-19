import io
import win32gui
import win32ui
import win32api
from PIL import Image
import ctypes

from fastmcp import FastMCP, Image as FastMCPImage

mcp: FastMCP = FastMCP(
    name="screencapture",
)


# this was mostly llm generated so if it doesn't work, blame the ai
@mcp.tool("screenshot_window")
async def screenshot_window(hwnd: int) -> str | FastMCPImage:
    """Capture a screenshot of the specified window handle (hwnd). Does not require the window to be visible."""
    try:
        hwnd = int(hwnd)
        if not win32gui.IsWindow(hwnd):
            return "Invalid window handle"

        # Get window rect
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        # Check for valid dimensions
        if width <= 0 or height <= 0:
            return "Window has invalid dimensions"

        # Get window device context
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # Change PrintWindow flags to capture entire window content including child windows
        # PW_RENDERFULLCONTENT = 0x00000002
        result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

        # Add a small delay to ensure the content is captured
        win32api.Sleep(100)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        # Check if we have valid bitmap data
        if not bmpstr or len(bmpstr) <= 0:
            return "Failed to capture window content"
            
        img = Image.frombuffer(
            "RGB",
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )

        # Cleanup
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if result:
            # Preserve aspect ratio when resizing
            if width > 0 and height > 0:
                target_width = 1024
                target_height = int(height * (target_width / width))
                
                # Make sure we don't exceed maximum height
                if target_height > 2048:
                    target_height = 2048
                    target_width = int(width * (target_height / height))
                
                img = img.resize((target_width, target_height), Image.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            return FastMCPImage(data=buffer.read(), format="png")
        else:
            return "Screenshot may be partial or failed due to permissions"
    except Exception as e:
        return f"Failed to capture screenshot: {type(e).__name__}: {e}"