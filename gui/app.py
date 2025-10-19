"""
Main application class for Natlink GUI
"""

import wx
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import load_grammars, LOADED
from addon_manager import install_addon
from .main_frame import GrammarManagerFrame


class NatlinkApp(wx.App):
    """Main application class"""
    
    def OnInit(self):
        """Initialize the application"""
        # Handle command line arguments
        self._handle_command_line()
        
      
        
        # Create and show main frame
        self.frame = GrammarManagerFrame()
        
        # Load grammars and log them
        self.frame.log_msg("🔄 Loading grammars...")
        load_grammars()
        
        # Log loaded grammars
        if LOADED:
            for name, module in LOADED.items():
                # Try to get addon info
                addon_name = getattr(module, '__file__', '')
                if addon_name:
                    addon_path = Path(addon_name).parent.name
                    self.frame.log_msg(f"✅ Loaded grammar: {name} ({addon_path})")
                else:
                    self.frame.log_msg(f"✅ Loaded grammar: {name}")
            self.frame.log_msg(f"📊 Total grammars loaded: {len(LOADED)}")
        else:
            self.frame.log_msg("⚠️ No grammars found")
        
        self.frame.log_msg("")
        self.frame.Show()
        
        return True
    
    def _handle_command_line(self):
        """Handle command line arguments for addon installation"""
        if len(sys.argv) > 1:
            addon_file = Path(sys.argv[1])
            if addon_file.suffix == ".addon-natlink" and addon_file.exists():
                install_addon(addon_file)
            else:
                print(f"⚠️ Invalid addon file: {addon_file}")
