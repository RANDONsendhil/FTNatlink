"""
Splash screen for FTNatlink application
Shows loading information while the app initializes
"""

import wx
import wx.adv
import threading
import time
from pathlib import Path

# Add parent directory to path for imports
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logHandler import log


class SplashScreen(wx.adv.SplashScreen):
    """Splash screen with loading progress"""

    def __init__(self):
        # Ensure wx.App is initialized before creating bitmaps
        if not wx.GetApp():
            raise RuntimeError("wx.App must be created before SplashScreen")

        # Create a simple bitmap for the splash (optimized for speed)
        bitmap = self._create_simple_splash_bitmap()

        super().__init__(
            bitmap,
            wx.adv.SPLASH_CENTRE_ON_SCREEN,  # Removed SPLASH_TIMEOUT
            0,  # No timeout - manual control only
            None,
            -1,
            style=wx.BORDER_SIMPLE | wx.FRAME_NO_TASKBAR,
        )

        self.manual_close_allowed = False  # Prevent auto close
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        log.info("Splash screen displayed")

    def _create_simple_splash_bitmap(self):
        """Create a simpler, faster-loading bitmap for immediate display"""
        # Create bitmap with solid background first (faster)
        bitmap = wx.Bitmap(400, 300)
        dc = wx.MemoryDC(bitmap)

        # Simple solid background instead of gradient (faster)
        dc.SetBackground(wx.Brush(wx.Colour(35, 35, 45)))  # Dark blue-gray
        dc.Clear()

        # Title (essential content only)
        dc.SetTextForeground(wx.Colour(255, 255, 255))
        font = wx.Font(
            20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        dc.SetFont(font)

        title = "FTNatlink"
        title_size = dc.GetTextExtent(title)
        dc.DrawText(title, (400 - title_size.width) // 2, 100)

        # Subtitle
        font = wx.Font(
            12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        dc.SetFont(font)
        subtitle = "Voice Control Grammar Manager"
        subtitle_size = dc.GetTextExtent(subtitle)
        dc.DrawText(subtitle, (400 - subtitle_size.width) // 2, 140)

        # Loading text
        dc.SetTextForeground(wx.Colour(100, 200, 255))
        font = wx.Font(
            10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        dc.SetFont(font)
        loading_text = "Démarrage..."
        loading_size = dc.GetTextExtent(loading_text)
        dc.DrawText(loading_text, (400 - loading_size.width) // 2, 180)

        # Simple progress bar placeholder
        dc.SetPen(wx.Pen(wx.Colour(80, 80, 80), 1))
        dc.SetBrush(wx.Brush(wx.Colour(50, 50, 50)))
        dc.DrawRectangle(50, 220, 300, 15)

        dc.SelectObject(wx.NullBitmap)
        return bitmap

    def _create_splash_bitmap(self):
        """Create a full bitmap for the splash screen with gradient (used for updates)"""
        # Create a simple colored bitmap
        bitmap = wx.Bitmap(400, 300)
        dc = wx.MemoryDC(bitmap)

        # Background gradient
        dc.GradientFillLinear(
            wx.Rect(0, 0, 400, 300),
            wx.Colour(45, 45, 55),  # Dark blue-gray
            wx.Colour(25, 25, 35),  # Darker
            wx.SOUTH,
        )

        # Title
        dc.SetTextForeground(wx.Colour(255, 255, 255))
        font = wx.Font(
            20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        dc.SetFont(font)

        title = "FTNatlink"
        title_size = dc.GetTextExtent(title)
        dc.DrawText(title, (400 - title_size.width) // 2, 80)

        # Subtitle
        font = wx.Font(
            12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        dc.SetFont(font)
        subtitle = "Voice Control Grammar Manager"
        subtitle_size = dc.GetTextExtent(subtitle)
        dc.DrawText(subtitle, (400 - subtitle_size.width) // 2, 120)

        # Version
        font = wx.Font(
            10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL
        )
        dc.SetFont(font)
        dc.SetTextForeground(wx.Colour(200, 200, 200))
        version = "v1.0.0"
        version_size = dc.GetTextExtent(version)
        dc.DrawText(version, (400 - version_size.width) // 2, 145)

        # Loading area (will be updated)
        dc.SetTextForeground(wx.Colour(100, 200, 255))
        font = wx.Font(
            9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        dc.SetFont(font)
        loading_text = "Initialisation..."
        loading_size = dc.GetTextExtent(loading_text)
        dc.DrawText(loading_text, (400 - loading_size.width) // 2, 200)

        # Progress bar background
        dc.SetPen(wx.Pen(wx.Colour(80, 80, 80), 1))
        dc.SetBrush(wx.Brush(wx.Colour(40, 40, 40)))
        dc.DrawRectangle(50, 230, 300, 20)

        # Initial progress bar
        dc.SetBrush(wx.Brush(wx.Colour(100, 200, 255)))
        dc.DrawRectangle(52, 232, 30, 16)  # Small initial progress

        dc.SelectObject(wx.NullBitmap)
        return bitmap

    def _add_loading_text(self):
        """Add loading text overlay"""
        # This will be updated by the loading process
        pass

    def update_progress(self, message, progress=0):
        """Update the splash screen with loading progress"""
        log.info(f"🔄 Splash update_progress called: '{message}' - {progress}%")
        wx.CallAfter(self._simple_update_only, message, progress)

    def _simple_update_only(self, message, progress):
        """Simple update - only change title to avoid visual conflicts"""
        log.info(f"🎨 Simple update: '{message}' - {progress}%")
        try:
            if self.IsShown():
                # Just update window title with progress
                self.SetTitle(f"FTNatlink - {message} ({progress}%)")
                # No bitmap redraw to avoid double rendering
        except Exception as e:
            log.warning(f"Erreur mise à jour splash: {e}")

    def _do_update_progress(self, message, progress):
        """Actually update the progress (called on main thread)"""
        log.info(f"🎨 Splash _do_update_progress executing: '{message}' - {progress}%")
        log.info(f"Loading: {message}")

        try:
            # Get the current bitmap and update it
            bitmap = wx.Bitmap(400, 300)
            dc = wx.MemoryDC(bitmap)

            # Redraw background
            dc.GradientFillLinear(
                wx.Rect(0, 0, 400, 300),
                wx.Colour(45, 45, 55),
                wx.Colour(25, 25, 35),
                wx.SOUTH,
            )

            # Redraw static elements
            dc.SetTextForeground(wx.Colour(255, 255, 255))
            font = wx.Font(
                20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
            )
            dc.SetFont(font)

            title = "FTNatlink"
            title_size = dc.GetTextExtent(title)
            dc.DrawText(title, (400 - title_size.width) // 2, 80)

            font = wx.Font(
                12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
            )
            dc.SetFont(font)
            subtitle = "Voice Control Grammar Manager"
            subtitle_size = dc.GetTextExtent(subtitle)
            dc.DrawText(subtitle, (400 - subtitle_size.width) // 2, 120)

            font = wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL
            )
            dc.SetFont(font)
            dc.SetTextForeground(wx.Colour(200, 200, 200))
            version = "v1.0.0"
            version_size = dc.GetTextExtent(version)
            dc.DrawText(version, (400 - version_size.width) // 2, 145)

            # Update loading message
            dc.SetTextForeground(wx.Colour(100, 200, 255))
            font = wx.Font(
                9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
            )
            dc.SetFont(font)
            loading_size = dc.GetTextExtent(message)
            dc.DrawText(message, (400 - loading_size.width) // 2, 200)

            # Update progress bar
            dc.SetPen(wx.Pen(wx.Colour(80, 80, 80), 1))
            dc.SetBrush(wx.Brush(wx.Colour(40, 40, 40)))
            dc.DrawRectangle(50, 230, 300, 20)

            # Progress fill
            progress_width = int((progress / 100.0) * 296)  # 296 = 300 - 4 (padding)
            if progress_width > 0:
                dc.SetBrush(wx.Brush(wx.Colour(100, 200, 255)))
                dc.DrawRectangle(52, 232, progress_width, 16)

            dc.SelectObject(wx.NullBitmap)

            # Update the splash screen
            if self and self.IsShown():
                self.SetBitmap(bitmap)
                self.Refresh()
                self.Update()

        except Exception as e:
            log.warning(f"Erreur mise à jour splash: {e}")

    def _simple_update(self, message, progress):
        """Simple update without full redraw"""
        try:
            if self.IsShown():
                self.SetTitle(f"FTNatlink - {message}")
                self.Refresh()
        except:
            pass  # Ignore les erreurs

    def OnClose(self, event):
        """Handle splash screen close"""
        if not self.manual_close_allowed:
            log.info("Splash screen close prevented - not yet allowed")
            return  # Block automatic closing

        log.info("Splash screen closed")
        self.Destroy()

    def allow_close(self):
        """Allow manual closing of splash screen"""
        self.manual_close_allowed = True


class SimpleLoadingFrame(wx.Frame):
    """Simple loading frame as alternative to splash screen"""

    def __init__(self):
        super().__init__(
            None,
            title="FTNatlink - Chargement...",
            size=(350, 150),
            style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER | wx.STAY_ON_TOP,
        )

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(50, 50, 60))

        # Create sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(self.panel, label="🎤 FTNatlink")
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        title_font = title.GetFont()
        title_font.PointSize += 6
        title_font = title_font.Bold()
        title.SetFont(title_font)

        # Loading message
        self.loading_msg = wx.StaticText(
            self.panel, label="🔄 Initializing application..."
        )
        self.loading_msg.SetForegroundColour(wx.Colour(100, 200, 255))

        # Progress gauge
        self.progress = wx.Gauge(self.panel, range=100, size=(300, 20))
        self.progress.SetValue(0)

        # Layout
        sizer.AddSpacer(15)
        sizer.Add(title, 0, wx.CENTER)
        sizer.AddSpacer(10)
        sizer.Add(self.loading_msg, 0, wx.CENTER)
        sizer.AddSpacer(10)
        sizer.Add(self.progress, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 20)
        sizer.AddSpacer(15)

        self.panel.SetSizer(sizer)

        # Center on screen
        self.Centre()

        log.info("Loading frame displayed")

    def update_progress(self, message, progress=0):
        """Update loading progress - improved threading safety"""
        if wx.GetApp():
            wx.CallAfter(self._do_update, message, progress)
        else:
            self._do_update(message, progress)

    def _do_update(self, message, progress):
        """Update on main thread - improved error handling"""
        try:
            if self.loading_msg and not self.loading_msg.IsBeingDeleted():
                self.loading_msg.SetLabel(message)
            if self.progress and not self.progress.IsBeingDeleted():
                self.progress.SetValue(min(100, max(0, progress)))
            if not self.IsBeingDeleted():
                self.Refresh()
                self.Update()  # Force immediate update
            log.info(f"Loading: {message} ({progress}%)")
        except Exception as e:
            log.error(f"Error updating progress: {e}")

    def close_safely(self):
        """Safely close the loading frame"""
        try:
            if not self.IsBeingDeleted():
                wx.CallAfter(self.Close)
        except Exception as e:
            log.error(f"Error closing loading frame: {e}")
