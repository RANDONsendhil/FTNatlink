"""
Addons installation and management tab
"""

import wx
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from addon_manager import install_addon
from core.grammar_loader import reload_grammars


def create_addons_tab(parent, frame):
    """Create the Addons installation tab"""
    panel = wx.Panel(parent)
    
    # Title
    title = wx.StaticText(panel, label="Addon Management")
    title_font = title.GetFont()
    title_font.PointSize += 2
    title_font = title_font.Bold()
    title.SetFont(title_font)
    
    # Instructions
    instructions = wx.StaticText(panel, label=
        "Install voice command addons from .addon-natlink files.\n\n"
        "You can:\n"
        "• Install addons from your computer\n"
        "• Package your own addons\n"
        "• Share addons with others"
    )
    
    # Install button
    install_btn = wx.Button(panel, label="📦 Install Addon from File")
    install_btn.SetFont(install_btn.GetFont().Bold())
    
    # Package button
    package_info = wx.StaticText(panel, label=
        "\nTo create addon packages:\n"
        "Use: python addon_packager.py addons/your_addon"
    )
    package_info.SetForegroundColour(wx.Colour(100, 100, 100))
    
    # Bind events
    install_btn.Bind(wx.EVT_BUTTON, lambda e: on_install(e, frame))
    
    # Layout
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(title, 0, wx.ALL, 10)
    sizer.Add(instructions, 0, wx.ALL|wx.EXPAND, 10)
    sizer.Add(install_btn, 0, wx.CENTER|wx.ALL, 20)
    sizer.Add(package_info, 0, wx.ALL, 10)
    sizer.AddStretchSpacer()
    
    panel.SetSizer(sizer)
    return panel


def on_install(event, frame):
    """Open file dialog to select and install an addon"""
    frame.log_msg("\n📂 Opening file browser...")
    
    with wx.FileDialog(
        frame, 
        "Select Natlink Addon to Install",
        wildcard="Natlink Addon (*.addon-natlink)|*.addon-natlink|All files (*.*)|*.*",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    ) as dlg:
        if dlg.ShowModal() == wx.ID_CANCEL:
            frame.log_msg("❌ Installation cancelled by user")
            return
        
        addon_path = dlg.GetPath()
        frame.log_msg(f"📦 Selected: {Path(addon_path).name}")
        frame.log_msg("⏳ Installing addon...")
        
        try:
            # Install the addon
            install_addon(addon_path)
            frame.log_msg("✅ Addon installed successfully!")
            
            # Reload grammars to activate new addon
            frame.log_msg("♻️ Reloading grammars...")
            reload_grammars()
            frame.log_msg("✅ Grammars reloaded!")
            
            # Show success message
            wx.MessageBox(
                f"Addon installed successfully!\n\nFile: {Path(addon_path).name}\n\nGrammars have been reloaded.",
                "Installation Complete",
                wx.OK | wx.ICON_INFORMATION
            )
            
            # Refresh grammar list if the method exists
            if hasattr(frame, 'grammar_list'):
                from core.grammar_loader import list_grammars
                grammars = list_grammars()
                frame.grammar_list.Clear()
                
                if grammars:
                    for g in grammars:
                        frame.grammar_list.Append(f"📄 {g}")
            
        except FileNotFoundError as e:
            error_msg = f"File not found:\n{e}"
            frame.log_msg(f"❌ {error_msg}")
            wx.MessageBox(error_msg, "Installation Failed", wx.OK | wx.ICON_ERROR)
            
        except Exception as e:
            error_msg = f"Failed to install addon:\n{e}"
            frame.log_msg(f"❌ {error_msg}")
            wx.MessageBox(error_msg, "Installation Error", wx.OK | wx.ICON_ERROR)
