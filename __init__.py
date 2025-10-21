"""
FTNatlink - Main entry point
Natlink Grammar Manager for Dragon NaturallySpeaking voice commands
"""

import wx
import os
import sys
import threading
import time
import subprocess
import wx.adv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging first
from core.logging_config import get_logger, setup_logging

setup_logging()
log = get_logger(__name__)

from core import load_grammars, LOADED
from addon_manager import install_addon
from gui.main_frame import GrammarManagerFrame

log.info(f"wx version: {wx.VERSION_STRING}")
log.info(f"wx.adv available: {hasattr(wx, 'adv')}")
__all__ = ["main"]


# Handle PyInstaller path resolution
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


ICON_PATH = get_resource_path("icons/FTNatlink_DARK_BLUE.jpg")


def main():
    """Launch the tray application"""
    app = MainApp(False)
    app.MainLoop()


class TaskBarIcon(wx.adv.TaskBarIcon):
    """System tray icon with menu actions."""

    def __init__(self, frame):
        super(TaskBarIcon, self).__init__()
        self.frame = frame
        self.grammar_window = None  # Store reference to grammar window
        self.set_icon()

        # Bind events
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)

    def CreatePopupMenu(self):
        """Create right-click menu."""
        menu = wx.Menu()
        menu.Append(1, "Show Status")
        menu.Append(2, "GUI Grammar Manager")
        menu.Append(3, "Reload Grammars")
        menu.AppendSeparator()
        menu.Append(4, "Restart")
        menu.Append(5, "Quit")

        self.Bind(wx.EVT_MENU, self.on_menu_item, id=1)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=2)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=3)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=4)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=5)
        return menu

    def set_icon(self):
        """Use your custom FTNATLINK icon."""
        img = wx.Image(ICON_PATH, wx.BITMAP_TYPE_ANY)
        img = img.Scale(32, 32, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(img)
        icon = wx.Icon()
        icon.CopyFromBitmap(bmp)
        self.SetIcon(icon, "FTNatLink")

    def on_left_click(self, event):
        """Left-click shows the same menu."""
        self.PopupMenu(self.CreatePopupMenu())

    def on_menu_item(self, event):
        """Handle menu item actions."""
        eid = event.GetId()

        if eid == 1:
            self.show_status()
        elif eid == 2:
            self.open_grammar_manager()
        elif eid == 3:
            self.reload_grammars()
        elif eid == 4:
            self.restart_app()
        elif eid == 5:
            self.quit_app()

    def open_grammar_manager(self):
        """Open or show the grammar manager window."""
        if self.grammar_window is None or not self.grammar_window:
            # Create new window
            self.grammar_window = GrammarManagerFrame()

            # Display already loaded grammars (loaded on startup)
            self.grammar_window.log_msg("� Grammar Manager - Current Status:")

            # Log loaded grammars
            if LOADED:
                for name, module in LOADED.items():
                    # Try to get addon info
                    addon_name = getattr(module, "__file__", "")
                    if addon_name:
                        addon_path = Path(addon_name).parent.name
                        self.grammar_window.log_msg(
                            f"✅ Active grammar: {name} ({addon_path})"
                        )
                    else:
                        self.grammar_window.log_msg(f"✅ Active grammar: {name}")
                self.grammar_window.log_msg(f"📊 Total active grammars: {len(LOADED)}")
            else:
                self.grammar_window.log_msg("⚠️ No grammars currently active")

            self.grammar_window.log_msg("")

            # Bind close event to hide instead of destroy
            self.grammar_window.Bind(wx.EVT_CLOSE, self.on_grammar_window_close)

        # Show the window
        self.grammar_window.Show()
        self.grammar_window.Raise()

    def on_grammar_window_close(self, event):
        """Handle grammar window close - hide instead of destroy."""
        self.grammar_window.Hide()

    def show_status(self):
        """Show current application status."""
        if LOADED:
            grammar_list = "\n".join([f"• {name}" for name in LOADED.keys()])
            message = f"FTNatlink is running in background.\n\nLoaded grammars ({len(LOADED)}):\n{grammar_list}"
        else:
            message = (
                "FTNatlink is running in background.\n\nNo grammars currently loaded."
            )

        wx.MessageBox(message, "FTNatlink Status", wx.OK | wx.ICON_INFORMATION)

    def reload_grammars(self):
        """Reload all grammars."""
        try:
            log.info("🔄 Reloading grammars...")

            # Clear existing grammars first
            LOADED.clear()

            # Reload grammars
            load_grammars()

            # Log results
            if LOADED:
                for name, module in LOADED.items():
                    addon_name = getattr(module, "__file__", "")
                    if addon_name:
                        addon_path = Path(addon_name).parent.name
                        log.info(f"✅ Reloaded grammar: {name} ({addon_path})")
                    else:
                        log.info(f"✅ Reloaded grammar: {name}")
                log.info(f"📊 Total grammars reloaded: {len(LOADED)}")

                wx.MessageBox(
                    f"Successfully reloaded {len(LOADED)} grammar(s)!",
                    "Reload Complete",
                    wx.OK | wx.ICON_INFORMATION,
                )
            else:
                log.warning("⚠️ No grammars found after reload")
                wx.MessageBox(
                    "No grammars found to load.",
                    "Reload Complete",
                    wx.OK | wx.ICON_WARNING,
                )

        except Exception as e:
            log.error(f"❌ Error reloading grammars: {e}")
            wx.MessageBox(
                f"Error reloading grammars:\n{e}", "Reload Error", wx.OK | wx.ICON_ERROR
            )

    def restart_app(self):
        """Restart the app properly by cleaning up current instance first."""
        try:
            log.info("Restarting application...")

            # Stop background thread first
            app = wx.GetApp()
            if hasattr(app, "stop_background_task"):
                app.stop_background_task()

            # Clean up grammar window if it exists
            if self.grammar_window:
                self.grammar_window.Destroy()
                self.grammar_window = None

            # Clean up tray icon
            self.Destroy()

            # Schedule the restart after cleanup
            wx.CallAfter(self._perform_restart)

        except Exception as e:
            log.error(f"Error during restart cleanup: {e}")
            self._perform_restart()

    def _perform_restart(self):
        """Perform the actual restart after cleanup."""
        try:
            # Close the current app frame
            if hasattr(self, "frame") and self.frame:
                self.frame.Close()

            # Start new instance
            python = sys.executable
            subprocess.Popen([python] + sys.argv)

            # Exit current process
            wx.GetApp().ExitMainLoop()

            # Force exit if MainLoop doesn't work
            wx.CallLater(2000, lambda: os._exit(0))

        except Exception as e:
            log.error(f"Error during restart: {e}")
            os._exit(0)

    def quit_app(self):
        """Properly quit the application with cleanup."""
        try:
            log.info("Quitting application...")

            # Stop background thread first
            app = wx.GetApp()
            if hasattr(app, "stop_background_task"):
                app.stop_background_task()

            # Clean up grammar window if it exists
            if self.grammar_window:
                self.grammar_window.Destroy()
                self.grammar_window = None

            # Clean up tray icon
            self.Destroy()

            # Close main frame
            if hasattr(self, "frame") and self.frame:
                self.frame.Close()

            # Exit the application
            wx.CallAfter(self._force_exit)

        except Exception as e:
            log.error(f"Error during quit: {e}")
            # Force exit if cleanup fails
            wx.CallAfter(self._force_exit)

    def _force_exit(self):
        """Force application exit."""
        try:
            wx.GetApp().ExitMainLoop()
        except:
            pass

        # As a last resort, force exit the process
        wx.CallLater(1000, lambda: os._exit(0))


class MainApp(wx.App):
    """Main application class that runs in the background."""

    def OnInit(self):
        self.frame = wx.Frame(None)  # Invisible frame
        self.frame.Hide()
        self._running = True  # Flag to control background thread

        # Load grammars on startup
        log.info("🔄 Loading grammars on startup...")
        load_grammars()

        # Log loaded grammars
        if LOADED:
            for name, module in LOADED.items():
                addon_name = getattr(module, "__file__", "")
                if addon_name:
                    addon_path = Path(addon_name).parent.name
                    log.info(f"✅ Loaded grammar: {name} ({addon_path})")
                else:
                    log.info(f"✅ Loaded grammar: {name}")
            log.info(f"📊 Total grammars loaded: {len(LOADED)}")
        else:
            log.warning("⚠️ No grammars found")

        log.info("")  # Empty line for readability

        # Start tray icon
        self.taskbar_icon = TaskBarIcon(self.frame)

        # Start background thread
        threading.Thread(target=self.background_task, daemon=True).start()
        return True

    def background_task(self):
        """Example background work."""
        while self._running:
            log.debug("Background process running...")
            time.sleep(10)
        log.info("Background process stopped.")

    def stop_background_task(self):
        """Stop the background thread."""
        self._running = False


if __name__ == "__main__":
    app = MainApp(False)
    app.MainLoop()
