"""
Grammars management tab with split-view interface
"""

import wx
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.grammar_loader import list_grammars, load_grammars, unload_grammars, reload_grammars

GRAMMAR_DIR = Path(__file__).parent.parent.parent / "grammars"
ADDON_DIR = Path(__file__).parent.parent.parent / "addons"


def find_grammar_file(grammar_name):
    """Find grammar file in any of the three locations."""
    if not grammar_name.endswith('.py'):
        grammar_name = f"{grammar_name}.py"
    
    # Location 1: Direct in grammars/
    grammar_file = GRAMMAR_DIR / grammar_name
    if grammar_file.exists():
        return grammar_file
    
    # Location 2: In grammars subdirectories (installed addons)
    if GRAMMAR_DIR.exists():
        for subdir in GRAMMAR_DIR.iterdir():
            if subdir.is_dir():
                grammar_file = subdir / grammar_name
                if grammar_file.exists():
                    return grammar_file
    
    # Location 3: In addons/ folder (development addons)
    if ADDON_DIR.exists():
        for addon_folder in ADDON_DIR.iterdir():
            if addon_folder.is_dir():
                addon_json = addon_folder / "addon.json"
                if addon_json.exists():
                    grammar_file = addon_folder / grammar_name
                    if grammar_file.exists():
                        return grammar_file
    
    return None


def create_grammars_tab(parent, frame):
    """Create the Grammars management tab with split view"""
    panel = wx.Panel(parent)
    
    # Create splitter window
    splitter = wx.SplitterWindow(panel, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
    
    # Left panel - Grammar list
    left_panel = wx.Panel(splitter)
    
    # Title for left side
    left_title = wx.StaticText(left_panel, label="Available Grammars")
    left_title_font = left_title.GetFont()
    left_title_font.PointSize += 1
    left_title_font = left_title_font.Bold()
    left_title.SetFont(left_title_font)
    
    # Grammar list
    frame.grammar_list = wx.ListBox(left_panel, style=wx.LB_SINGLE)
    frame.grammar_list.Bind(wx.EVT_LISTBOX, lambda e: on_grammar_selected(e, frame))
    
    # Buttons
    list_btn = wx.Button(left_panel, label="📋 Refresh")
    load_btn = wx.Button(left_panel, label="⬇️ Load All")
    reload_btn = wx.Button(left_panel, label="♻️ Reload All")
    unload_btn = wx.Button(left_panel, label="⬆️ Unload All")
    
    # Bind events
    list_btn.Bind(wx.EVT_BUTTON, lambda e: on_list(e, frame))
    load_btn.Bind(wx.EVT_BUTTON, lambda e: on_load(e, frame))
    reload_btn.Bind(wx.EVT_BUTTON, lambda e: on_reload(e, frame))
    unload_btn.Bind(wx.EVT_BUTTON, lambda e: on_unload(e, frame))
    
    # Layout for left panel
    button_sizer = wx.GridSizer(2, 2, 5, 5)
    button_sizer.Add(list_btn, 0, wx.EXPAND)
    button_sizer.Add(load_btn, 0, wx.EXPAND)
    button_sizer.Add(reload_btn, 0, wx.EXPAND)
    button_sizer.Add(unload_btn, 0, wx.EXPAND)
    
    left_sizer = wx.BoxSizer(wx.VERTICAL)
    left_sizer.Add(left_title, 0, wx.ALL, 10)
    left_sizer.Add(frame.grammar_list, 1, wx.EXPAND|wx.ALL, 5)
    left_sizer.Add(button_sizer, 0, wx.EXPAND|wx.ALL, 5)
    
    left_panel.SetSizer(left_sizer)
    
    # Right panel - Grammar details
    right_panel = wx.Panel(splitter)
    
    # Title for right side
    right_title = wx.StaticText(right_panel, label="Grammar Details")
    right_title_font = right_title.GetFont()
    right_title_font.PointSize += 1
    right_title_font = right_title_font.Bold()
    right_title.SetFont(right_title_font)
    
    # Grammar info display
    frame.grammar_name_label = wx.StaticText(right_panel, label="Name: (Select a grammar)")
    frame.grammar_name_label.SetFont(frame.grammar_name_label.GetFont().Bold())
    
    # Details text area
    frame.grammar_details = wx.TextCtrl(
        right_panel, 
        style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
        size=(300, -1)
    )
    frame.grammar_details.SetValue("Select a grammar from the list to view details...")
    
    # Layout for right panel
    right_sizer = wx.BoxSizer(wx.VERTICAL)
    right_sizer.Add(right_title, 0, wx.ALL, 10)
    right_sizer.Add(frame.grammar_name_label, 0, wx.ALL, 10)
    right_sizer.Add(wx.StaticLine(right_panel), 0, wx.EXPAND|wx.ALL, 5)
    right_sizer.Add(wx.StaticText(right_panel, label="Information:"), 0, wx.ALL, 5)
    right_sizer.Add(frame.grammar_details, 1, wx.EXPAND|wx.ALL, 5)
    
    right_panel.SetSizer(right_sizer)
    
    # Split the window
    splitter.SplitVertically(left_panel, right_panel)
    splitter.SetSashPosition(350)
    splitter.SetMinimumPaneSize(200)
    
    # Main layout
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(splitter, 1, wx.EXPAND)
    
    panel.SetSizer(main_sizer)
    return panel


def on_grammar_selected(event, frame):
    """Display details when a grammar is selected"""
    selection = frame.grammar_list.GetStringSelection()
    if not selection or selection == "(No grammars found)":
        frame.grammar_name_label.SetLabel("Grammar Details")
        frame.grammar_details.SetValue("No grammar selected")
        return
    
    # Extract grammar name (remove the emoji prefix)
    grammar_stem = selection.replace("📄 ", "").strip()
    frame.grammar_name_label.SetLabel(f"Grammar: {grammar_stem}")
    
    # Find grammar file in any of the three locations
    grammar_file = find_grammar_file(grammar_stem)
    if not grammar_file:
        frame.grammar_details.SetValue(
            f"❌ Grammar file not found: {grammar_stem}\n\n"
            f"Searched in:\n"
            f"  • grammars/{grammar_stem}.py\n"
            f"  • grammars/*/{grammar_stem}.py\n"
            f"  • addons/*/{grammar_stem}.py"
        )
        return
    
    # Get the grammar name with extension for addon search
    grammar_name = grammar_file.name
    
    try:
        # Read the file content
        with open(grammar_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract information
        details = []
        details.append(f"📄 File: {grammar_file.name}")
        details.append(f"📂 Location: {grammar_file.parent}")
        details.append(f"📏 Size: {len(content)} characters\n")
        
        # Try to extract docstring
        import ast
        try:
            tree = ast.parse(content)
            # Get module docstring
            if ast.get_docstring(tree):
                details.append("📝 Description:")
                details.append(ast.get_docstring(tree))
                details.append("")
            
            # Find classes and their methods
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    details.append(f"🔷 Class: {node.name}")
                    if ast.get_docstring(node):
                        details.append(f"   {ast.get_docstring(node)}")
                    
                    # List methods
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    if methods:
                        details.append(f"   Methods: {', '.join(methods)}")
                    details.append("")
            
            # Look for command definitions (dictionaries)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and 'command' in target.id.lower():
                            if isinstance(node.value, ast.Dict):
                                details.append("🎤 Voice Commands:")
                                for key in node.value.keys:
                                    if isinstance(key, ast.Constant):
                                        details.append(f"   • \"{key.value}\"")
                                details.append("")
                                break
        
        except SyntaxError:
            details.append("⚠️ Could not parse Python syntax")
        
        # Check for addon.json
        addon_info = None
        
        # First, check if the grammar file is directly in an addon folder
        if grammar_file.parent.name != "grammars":
            # Check if parent folder has addon.json
            addon_json = grammar_file.parent / "addon.json"
            if addon_json.exists():
                try:
                    with open(addon_json, 'r', encoding='utf-8') as f:
                        addon_info = json.load(f)
                except:
                    pass
        
        # If not found, search all addon folders
        if not addon_info and ADDON_DIR.exists():
            for addon_folder in ADDON_DIR.iterdir():
                if addon_folder.is_dir():
                    addon_json = addon_folder / "addon.json"
                    if addon_json.exists():
                        try:
                            with open(addon_json, 'r', encoding='utf-8') as f:
                                addon_data = json.load(f)
                                # Check if this grammar is part of the addon
                                if grammar_name in addon_data.get("grammars", []):
                                    addon_info = addon_data
                                    break
                        except:
                            pass
        
        # Display addon information if found
        if addon_info:
            details.append("=" * 50)
            details.append("📦 ADDON INFORMATION")
            details.append("=" * 50)
            details.append(f"📦 Name: {addon_info.get('name', 'N/A')}")
            details.append(f"🔢 Version: {addon_info.get('version', 'N/A')}")
            details.append(f"📝 Description: {addon_info.get('description', 'N/A')}")
            details.append(f"👤 Author: {addon_info.get('author', 'N/A')}")
            
            if addon_info.get('grammars'):
                details.append(f"📄 Grammars: {', '.join(addon_info['grammars'])}")
            
            if addon_info.get('dependencies'):
                if addon_info['dependencies']:
                    details.append(f"📚 Dependencies: {', '.join(addon_info['dependencies'])}")
                else:
                    details.append("📚 Dependencies: None")
            
            details.append("")
        
        # Display the details
        frame.grammar_details.SetValue("\n".join(details))
        
    except Exception as e:
        frame.grammar_details.SetValue(f"❌ Error reading grammar:\n{str(e)}")


def on_list(event, frame):
    """Refresh the grammar list"""
    grammars = list_grammars()
    frame.grammar_list.Clear()
    
    if grammars:
        for g in grammars:
            frame.grammar_list.Append(f"📄 {g}")
        frame.log_msg(f"✅ Found {len(grammars)} grammar(s)")
    else:
        frame.grammar_list.Append("(No grammars found)")
        frame.log_msg("⚠️ No grammars found in grammars/ folder")


def on_load(event, frame):
    """Load all grammars"""
    load_grammars()
    frame.log_msg("✅ Grammars loaded.")


def on_reload(event, frame):
    """Reload all grammars"""
    reload_grammars()
    frame.log_msg("♻️ Grammars reloaded.")


def on_unload(event, frame):
    """Unload all grammars"""
    unload_grammars()
    frame.log_msg("🔻 Grammars unloaded.")
