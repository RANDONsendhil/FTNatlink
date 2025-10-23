#!/usr/bin/env python3
"""
Test script to verify splash screen functionality
"""

import wx
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.splash_screen import SimpleLoadingFrame
import time


class TestApp(wx.App):
    def OnInit(self):
        print("Creating loading frame...")
        self.frame = SimpleLoadingFrame()
        self.frame.Show()

        # Test progress updates
        wx.CallLater(500, self.test_progress)
        return True

    def test_progress(self):
        print("Testing progress updates...")
        self.frame.update_progress("🔍 Step 1: Testing...", 25)
        wx.CallLater(1000, self.test_progress2)

    def test_progress2(self):
        self.frame.update_progress("📝 Step 2: Loading...", 50)
        wx.CallLater(1000, self.test_progress3)

    def test_progress3(self):
        self.frame.update_progress("⚙️ Step 3: Finalizing...", 75)
        wx.CallLater(1000, self.test_complete)

    def test_complete(self):
        self.frame.update_progress("✅ Complete!", 100)
        wx.CallLater(2000, self.close_app)

    def close_app(self):
        print("Closing application...")
        self.frame.Close()
        wx.CallLater(500, self.Exit)


if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()
