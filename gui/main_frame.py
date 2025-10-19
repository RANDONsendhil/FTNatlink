"""
Main frame window for the Natlink Grammar Manager
"""

import wx
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .tabs.grammars_tab import create_grammars_tab
from .tabs.addons_tab import create_addons_tab
from .tabs.log_tab import create_log_tab


class GrammarManagerFrame(wx.Frame):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__(None, title="Natlink Grammar Manager", size=(900, 700))
        
        # Create notebook (tab container)
        self.notebook = wx.Notebook(self)
        
        # Create tabs
        self.grammars_panel = create_grammars_tab(self.notebook, self)
        self.addons_panel = create_addons_tab(self.notebook, self)
        self.log_panel = create_log_tab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.AddPage(self.grammars_panel, "📋 Grammars")
        self.notebook.AddPage(self.addons_panel, "📦 Addons")
        self.notebook.AddPage(self.log_panel, "📄 Log")
        
        # Main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Centre()
        
        # Log welcome message
        self.log_msg("🎤 Natlink Grammar Manager")
        self.log_msg("=" * 60)
        self.log_msg("Welcome! Use the tabs to manage your voice commands.")
        self.log_msg("=" * 60)
        self.log_msg("")
    
    def log_msg(self, text):
        """Add message to log"""
        if hasattr(self, 'log'):
            self.log.AppendText(text + "\n")
