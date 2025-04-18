"""this script registers a start menu shortcut for the MCP Windows app with a custom AppUserModelID.
This is necessary for the app to be able to send windows toast notifications due to some legacy UWP API
limitations.

If you press the windows key and type "mcp" in the start menu, you should see the MCP Windows app icon."""

import os
import sys
from win32com.client import Dispatch
import pythoncom

APP_ID = "mcp-windows"
SHORTCUT_PATH = os.path.join(
    os.environ["APPDATA"],
    r"Microsoft\Windows\Start Menu\Programs\MCP Windows.lnk"
)

STGM_READWRITE = 0x00000002

def register_app_id():
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(SHORTCUT_PATH)
    shortcut.TargetPath = sys.executable
    shortcut.WorkingDirectory = os.getcwd()
    shortcut.IconLocation = sys.executable
    shortcut.Save()

    # Add AppUserModelID
    from win32com.propsys import propsys, pscon
    property_store = propsys.SHGetPropertyStoreFromParsingName(SHORTCUT_PATH, None, STGM_READWRITE)
    property_store.SetValue(pscon.PKEY_AppUserModel_ID, propsys.PROPVARIANTType(APP_ID, pythoncom.VT_LPWSTR))
    property_store.Commit()

register_app_id()
