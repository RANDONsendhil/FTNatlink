"""
Main application class for Natlink GUI
"""

import wx
import sys
import time
import threading
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import load_grammars, LOADED
from addon_manager import install_addon
from .main_frame import GrammarManagerFrame
from .splash_screen import SimpleLoadingFrame
from core.logHandler import log


class NatlinkApp(wx.App):
    """Main application class"""

    def OnInit(self):
        """Initialize the application"""
        # Show loading screen immediately
        self.loading_frame = SimpleLoadingFrame()
        self.loading_frame.Show()

        # Process pending events to show the loading frame
        wx.GetApp().Yield()

        # Handle command line arguments
        self._handle_command_line()

        # Initialize in background thread to keep GUI responsive
        threading.Thread(target=self._initialize_app, daemon=True).start()

        return True

    def _initialize_app(self):
        """Initialize application in background thread"""
        try:
            # Step 1: Initialize components
            wx.CallAfter(
                self.loading_frame.update_progress,
                "Initialisation des composants...",
                20,
            )
            time.sleep(0.5)  # Small delay to show progress

            # Step 2: Load grammars
            wx.CallAfter(
                self.loading_frame.update_progress, "Chargement des grammaires...", 40
            )
            load_grammars()

            # Step 3: Create main frame
            wx.CallAfter(
                self.loading_frame.update_progress, "Création de l'interface...", 60
            )
            wx.CallAfter(self._create_main_frame)

        except Exception as e:
            log.error(f"Error during initialization: {e}")
            wx.CallAfter(self._show_error, str(e))

    def _create_main_frame(self):
        """Create main frame on main thread"""
        try:
            # Update progress
            self.loading_frame.update_progress("Configuration de l'interface...", 80)

            # Create main frame
            self.frame = GrammarManagerFrame()

            # Log loaded grammars to the main frame
            self.frame.log_msg("Chargement des grammaires terminé")

            if LOADED:
                for name, module in LOADED.items():
                    # Try to get addon info
                    addon_name = getattr(module, "__file__", "")
                    if addon_name:
                        addon_path = Path(addon_name).parent.name
                        self.frame.log_msg(f"Grammaire chargée : {name} ({addon_path})")
                    else:
                        self.frame.log_msg(f"Grammaire chargée : {name}")
                self.frame.log_msg(f"Total des grammaires chargées : {len(LOADED)}")
            else:
                self.frame.log_msg("Aucune grammaire trouvée")

            self.frame.log_msg("")

            # Final progress update
            self.loading_frame.update_progress("Prêt!", 100)
            time.sleep(0.5)  # Brief pause to show completion

            # Hide loading frame and show main frame
            self.loading_frame.Hide()
            self.loading_frame.Destroy()
            self.loading_frame = None

            self.frame.Show()
            self.frame.Raise()  # Bring to front

            # Refresh grammar list in the GUI after everything is loaded
            wx.CallAfter(self._refresh_grammar_tab)

            log.info("Application initialization completed")

        except Exception as e:
            log.error(f"Error creating main frame: {e}")
            self._show_error(str(e))

    def _refresh_grammar_tab(self):
        """Refresh the grammar tab to show loaded grammars"""
        try:
            # Import here to avoid circular imports
            from .tabs.grammars_tab import auto_refresh_grammars

            # Refresh the grammar list after a small delay to ensure everything is loaded
            wx.CallLater(500, lambda: auto_refresh_grammars(self.frame))

        except Exception as e:
            log.error(f"Error refreshing grammar tab: {e}")

    def _show_error(self, error_msg):
        """Show error dialog"""
        if self.loading_frame:
            self.loading_frame.Hide()
            self.loading_frame.Destroy()

        wx.MessageBox(
            f"Échec d'initialisation de l'application :\n{error_msg}",
            "Erreur d'Initialisation",
            wx.OK | wx.ICON_ERROR,
        )
        self.ExitMainLoop()

    def _handle_command_line(self):
        """Handle command line arguments for addon installation"""
        if len(sys.argv) > 1:
            addon_file = Path(sys.argv[1])
            if addon_file.suffix == ".addon-natlink" and addon_file.exists():
                install_addon(addon_file)
            else:
                print(f"⚠️ Invalid addon file: {addon_file}")
