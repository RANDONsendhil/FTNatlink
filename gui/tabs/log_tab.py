"""
Activity log tab for displaying application messages
"""

import wx


def create_log_tab(parent, frame):
    """Create the Log output tab"""
    panel = wx.Panel(parent)
    
    # Title
    title = wx.StaticText(panel, label="Activity Log")
    title_font = title.GetFont()
    title_font.PointSize += 2
    title_font = title_font.Bold()
    title.SetFont(title_font)
    
    # Log text area
    frame.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP)
    
    # Clear button
    clear_btn = wx.Button(panel, label="🗑️ Clear Log")
    clear_btn.Bind(wx.EVT_BUTTON, lambda e: frame.log.Clear())
    
    # Layout
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(title, 0, wx.ALL, 10)
    sizer.Add(frame.log, 1, wx.EXPAND|wx.ALL, 5)
    sizer.Add(clear_btn, 0, wx.CENTER|wx.ALL, 5)
    
    panel.SetSizer(sizer)
    return panel
