"""
Natlink GUI Module
Main entry point for the graphical user interface
"""

import wx
from .app import NatlinkApp

def main():
    """Launch the Natlink GUI application"""
    app = NatlinkApp()
    app.MainLoop()

__all__ = ['main', 'NatlinkApp']

# Allow running as: python -m gui
if __name__ == "__main__":
  
    main()
