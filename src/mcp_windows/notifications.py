import asyncio
from fastmcp import FastMCP

from mcp_windows.appid import APP_ID

from winrt.windows.ui.notifications import ToastNotificationManager, ToastNotification
from winrt.windows.data.xml.dom import XmlDocument

mcp: FastMCP = FastMCP(
    name="notifications",
)

@mcp.tool("send_toast")
async def send_toast(title: str, message: str) -> str:
    """Send a windows toast notification to the user."""


    toast_xml_string = f"""
    <toast>
        <visual>
            <binding template="ToastGeneric">
                <text>{title}</text>
                <text>{message}</text>
            </binding>
        </visual>
    </toast>
    """

    xml_doc = XmlDocument()
    xml_doc.load_xml(toast_xml_string)

    toast = ToastNotification(xml_doc)

    notifier = ToastNotificationManager.create_toast_notifier_with_id(APP_ID)

    notifier.show(toast)

    return "Toast notification sent"