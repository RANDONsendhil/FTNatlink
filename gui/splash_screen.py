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
        # Create a simple bitmap for the splash
        bitmap = self._create_splash_bitmap()

        super().__init__(
            bitmap,
            wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
            5000,  # 5 second timeout
            None,
            -1,
            style=wx.BORDER_SIMPLE | wx.FRAME_NO_TASKBAR,
        )

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Add loading text
        self._add_loading_text()

        log.info("Splash screen displayed")

    def _create_splash_bitmap(self):
        """Create a bitmap for the splash screen"""
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
        wx.CallAfter(self._do_update_progress, message, progress)

    def _do_update_progress(self, message, progress):
        """Actually update the progress (called on main thread)"""
        log.info(f"Loading: {message}")

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
        if self:
            self.SetBitmap(bitmap)
            self.Refresh()
            self.Update()

    def OnClose(self, event):
        """Handle splash screen close"""
        log.info("Splash screen closed")
        self.Destroy()


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
        """Update loading progress"""
        wx.CallAfter(self._do_update, message, progress)

    def _do_update(self, message, progress):
        """Update on main thread"""
        if self.loading_msg:
            self.loading_msg.SetLabel(message)
        if self.progress:
            self.progress.SetValue(progress)
        self.Refresh()
        log.info(f"Loading: {message} ({progress}%)")
