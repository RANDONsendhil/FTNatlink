"""
FTNatlink - Main entry point
Natlink Grammar Manager for Dragon NaturallySpeaking voice commands
"""

import wx
import os
import sys
import threading
import time
import subprocess
import wx.adv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# DEFER HEAVY IMPORTS - Only import wx and basic modules at startup
# Heavy imports will be done after splash screen is shown
__all__ = ["main"]


# Handle PyInstaller path resolution
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


ICON_PATH = get_resource_path("icons/FTNatlink_DARK_BLUE.jpg")


class TrayApp(wx.App):
    """Application hybride avec écran de démarrage et fonctionnement en tray."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = None
        self.tbicon = None
        self.splash = None
        self.mic_manager = None  # Gestionnaire d'état du micro Dragon
        self.instance_manager = None  # Gestionnaire d'instance unique
        self._log = None  # Lazy loading of logger
        self.loading_frame = None  # Loading frame reference

    @property
    def log(self):
        """Lazy load logger to avoid import delays at startup"""
        try:
            if not hasattr(self, "_log") or self._log is None:
                from core.logHandler import log

                self._log = log
            return self._log
        except Exception as e:
            # Fallback to print if logger fails
            print(f"Logger error: {e}")
            return type(
                "MockLogger",
                (),
                {
                    "info": lambda x: print(f"INFO: {x}"),
                    "error": lambda x: print(f"ERROR: {x}"),
                    "warning": lambda x: print(f"WARNING: {x}"),
                    "debug": lambda x: print(f"DEBUG: {x}"),
                },
            )()

    def OnInit(self):
        """Initialize the tray application with splash screen."""
        try:
            # FIRST: Show splash screen immediately before any heavy operations
            self.show_loading_frame()

            # Process pending events to ensure loading frame is shown
            wx.GetApp().Yield()

            # NOW setup logging and imports (after splash is visible)
            from core.logging_config import setup_logging

            setup_logging()

            self.log.info("Initialisation de l'application tray avec splash screen")
            self.log.info(f"wx version: {wx.VERSION_STRING}")
            self.log.info(f"wx.adv available: {hasattr(wx, 'adv')}")

            # Create a hidden main frame
            self.frame = wx.Frame(None, title="FTNatlink")
            self.frame.Hide()

            # Start all checks and loading in background thread (like NatlinkApp)
            wx.CallLater(100, self._background_init)

            return True

        except Exception as e:
            print(
                f"Erreur lors de l'initialisation: {e}"
            )  # Use print since log might not be available
            return False

    def show_loading_frame(self):
        """Show the SimpleLoadingFrame instead of SplashScreen"""
        try:
            print("DEBUG: Starting to create loading frame...")
            # Import SimpleLoadingFrame from gui
            from gui.splash_screen import SimpleLoadingFrame

            self.loading_frame = SimpleLoadingFrame()
            print(f"DEBUG: Created loading_frame: {self.loading_frame}")

            # Store a backup reference to prevent garbage collection
            self._loading_frame_backup = self.loading_frame

            self.loading_frame.Show()

            # Force a refresh and update to make sure it's visible
            self.loading_frame.Refresh()
            self.loading_frame.Update()
            print("DEBUG: Loading frame shown and updated")

            # Update loading frame with initial message
            if hasattr(self.loading_frame, "update_progress"):
                self.loading_frame.update_progress("🚀 Initializing FTNatlink...", 5)
                print("Loading frame created and initial progress set")
            else:
                print("ERROR: Loading frame does not have update_progress method")

        except Exception as e:
            print(f"Erreur lors de l'affichage du loading frame: {e}")
            import traceback

            traceback.print_exc()

    def _background_init(self):
        """Run initialization in background thread to keep splash responsive"""
        try:
            # Step 1: Single instance check
            wx.CallAfter(self._step1_single_instance_check)
        except Exception as e:
            self.log.error(f"Erreur lors de l'initialisation en arrière-plan: {e}")
            wx.CallAfter(self._handle_init_error, str(e))

    def _step1_single_instance_check(self):
        """Step 1: Check single instance"""
        try:
            # Update loading frame with current step - safer update
            self.log.info("🔄 Vérification instance unique...")
            self._safe_update_progress("🔍 Vérification instance unique...", 15)

            # CRITICAL: Check single instance AFTER loading frame is shown
            from core.single_instance import check_single_instance

            can_continue, instance_manager = check_single_instance()

            if not can_continue:
                self.log.warning("❌ Instance FTNatlink déjà active - arrêt")
                self._safe_update_progress("Instance déjà active - fermeture...", 100)
                wx.CallLater(1500, self._safe_close_loading_frame)
                wx.CallLater(2000, self._force_exit)
                return

            # Store instance manager for cleanup
            self.instance_manager = instance_manager
            self.log.info("✅ Instance unique confirmée")

            # Continue to next step
            wx.CallLater(100, self._step2_dragon_check)

        except Exception as e:
            self.log.error(f"Erreur lors de la vérification d'instance: {e}")
            wx.CallAfter(self._handle_init_error, str(e))

    def _safe_update_progress(self, message, progress):
        """Safely update progress with error handling"""
        try:
            # If main reference is lost, try backup
            if not self.loading_frame and hasattr(self, "_loading_frame_backup"):
                self.loading_frame = self._loading_frame_backup

            if self.loading_frame and hasattr(self.loading_frame, "update_progress"):
                # Since we're now using wx.CallLater instead of threading, we can call directly
                self.loading_frame.update_progress(message, progress)
                self.log.info(f"✅ Progress updated: {message} ({progress}%)")
            else:
                self.log.warning(f"Cannot update progress: {message} ({progress}%)")
        except Exception as e:
            self.log.error(f"Error updating progress: {e}")

    def _safe_close_loading_frame(self):
        """Safely close loading frame"""
        try:
            if self.loading_frame:
                if hasattr(self.loading_frame, "close_safely"):
                    self.loading_frame.close_safely()
                else:
                    wx.CallAfter(self.loading_frame.Close)
        except Exception as e:
            self.log.error(f"Error closing loading frame: {e}")

    def _step2_dragon_check(self):
        """Step 2: Dragon verification"""
        try:
            # Update loading frame
            self.log.info("🔄 Étape 1: Vérification Dragon...")
            self._safe_update_progress(
                "🐉 Vérification Dragon NaturallySpeaking...", 35
            )

            # Dragon verification
            from core.dragon_checker import (
                enforce_dragon_requirement,
                DragonVerificationError,
            )

            try:
                enforce_dragon_requirement()
                self.log.info(
                    "✅ Dragon NaturallySpeaking vérifié - continuation du chargement"
                )
            except DragonVerificationError as e:
                self.log.error(f"❌ Dragon NaturallySpeaking requis: {e}")
                if self.loading_frame:
                    self.loading_frame.Close()
                wx.CallAfter(self.ExitMainLoop)
                return

            # Continue to next step
            wx.CallLater(500, self._step3_load_grammars)

        except Exception as e:
            self.log.error(f"Erreur lors de la vérification Dragon: {e}")
            wx.CallAfter(self._handle_init_error, str(e))

    def _step3_load_grammars(self):
        """Step 3: Load grammars"""
        try:
            # Import grammar loading function
            from core.grammar_loader import load_grammars

            # Update loading frame
            self.log.info("🔄 Étape 2: Chargement des grammaires...")
            self._safe_update_progress(
                "📝 Chargement des grammaires...", 65
            )  # Load grammars
            self.log.info("Chargement des grammaires...")
            load_grammars()

            # Continue to final step
            wx.CallLater(500, self._step4_finish_init)

        except Exception as e:
            self.log.error(f"Erreur lors du chargement des grammaires: {e}")
            wx.CallAfter(self._handle_init_error, str(e))

    def _step4_finish_init(self):
        """Step 4: Finish initialization"""
        try:
            # Update loading frame
            self.log.info("🔄 Finalisation...")
            self._safe_update_progress("⚙️ Finalisation du démarrage...", 85)

            # Create tray icon
            self.tbicon = TaskBarIcon(self.frame)

            # Start microphone manager
            from core.mic_monitor import MicStateManager

            self.mic_manager = MicStateManager(self)

            if self.mic_manager.start():
                self.log.info("✅ Gestionnaire micro Dragon démarré")
            else:
                self.log.warning("⚠️ Impossible de démarrer le gestionnaire micro")

            # Final update with completion
            self._safe_update_progress("✅ Prêt! Démarrage terminé", 100)

            # Close loading frame after brief display
            wx.CallLater(1500, self._complete_startup)

            self.log.info("Application démarrée en mode tray")

        except Exception as e:
            self.log.error(f"Erreur lors de la finalisation: {e}")
            wx.CallAfter(self._handle_init_error, str(e))

    def _complete_startup(self):
        """Complete the startup and close loading frame properly"""
        try:
            if self.loading_frame:
                self.log.info("Fermeture du loading frame...")
                if hasattr(self.loading_frame, "close_safely"):
                    self.loading_frame.close_safely()
                else:
                    wx.CallAfter(self.loading_frame.Close)
                self.loading_frame = None
                self.log.info("Loading frame fermé avec succès")
        except Exception as e:
            self.log.error(f"Erreur lors de la fermeture du loading frame: {e}")

    def _handle_init_error(self, error_msg):
        """Handle initialization errors"""
        self.log.error(f"Erreur d'initialisation: {error_msg}")
        if self.loading_frame:
            self.loading_frame.Close()
        wx.CallAfter(self.ExitMainLoop)

    def show_splash_screen(self):
        """Affiche l'écran de démarrage."""
        try:
            # Import splash screen from gui
            from gui.splash_screen import SplashScreen

            self.splash = SplashScreen()
            self.splash.Show()

            # Update splash with loading message
            if hasattr(self.splash, "update_progress"):
                self.splash.update_progress("Chargement des grammaires...")

        except Exception as e:
            self.log.error(f"Erreur lors de l'affichage du splash screen: {e}")

    def initialize_background(self):
        """Initialize background components and hide splash."""
        try:
            # Update splash
            self.log.info("🔄 Étape 1: Vérification Dragon...")
            self.log.info(f"🔍 DEBUG: self.splash exists: {self.splash is not None}")
            if self.splash and hasattr(self.splash, "update_progress"):
                self.log.info("📊 FORCE: Appel update_progress 25%")
                self.splash.update_progress(
                    "Vérification de Dragon NaturallySpeaking...", 25
                )
                wx.SafeYield()  # Force immediate processing
            else:
                self.log.warning("❌ Splash screen unavailable for progress update 25%")

            # Small delay to see progress
            wx.MilliSleep(1500)

            # Vérifier Dragon AVANT de continuer
            from core.dragon_checker import (
                enforce_dragon_requirement,
                DragonVerificationError,
            )

            try:
                enforce_dragon_requirement()
                self.log.info(
                    "✅ Dragon NaturallySpeaking vérifié - continuation du chargement"
                )
            except DragonVerificationError as e:
                self.log.error(f"❌ Dragon NaturallySpeaking requis: {e}")
                # Fermer le splash et quitter
                if self.splash:
                    self.splash.Close()
                wx.CallAfter(self.ExitMainLoop)
                return

            # Update splash
            self.log.info("🔄 Étape 2: Configuration des modules...")
            if self.splash and hasattr(self.splash, "update_progress"):
                self.log.info("📊 FORCE: Appel update_progress 40%")
                self.splash.update_progress("Configuration des modules...", 40)
                wx.SafeYield()  # Force immediate processing

            wx.MilliSleep(1000)

            # Update splash
            self.log.info("🔄 Étape 3: Chargement des grammaires...")
            if self.splash and hasattr(self.splash, "update_progress"):
                self.log.info("📊 FORCE: Appel update_progress 60%")
                self.splash.update_progress("Chargement des grammaires...", 60)
                wx.SafeYield()  # Force immediate processing

            wx.MilliSleep(200)

            # Load grammars
            self.log.info("Chargement des grammaires...")
            load_grammars()

            # Update splash
            self.log.info("🔄 Étape 4: Finalisation des grammaires...")
            if self.splash and hasattr(self.splash, "update_progress"):
                self.splash.update_progress("Finalisation des grammaires...", 80)

            wx.MilliSleep(200)

            # Update splash
            self.log.info("🔄 Étape 5: Initialisation du système tray...")
            if self.splash and hasattr(self.splash, "update_progress"):
                self.splash.update_progress("Initialisation du système tray...", 90)

            wx.MilliSleep(200)

            # Wait a moment for visibility
            wx.CallLater(500, self.finish_initialization)

        except Exception as e:
            self.log.error(f"Erreur lors de l'initialisation en arrière-plan: {e}")
            # En cas d'erreur, fermer proprement
            if self.splash:
                self.splash.Close()
            wx.CallAfter(self.ExitMainLoop)

    def finish_initialization(self):
        """Finish initialization, hide splash, show tray icon."""
        try:
            # Update splash to show completion
            if self.splash and hasattr(self.splash, "update_progress"):
                self.splash.update_progress("Démarrage final...", 95)

            # Create tray icon
            self.tbicon = TaskBarIcon(self.frame)

            # Démarrer le gestionnaire d'état du micro Dragon
            from core.mic_monitor import MicStateManager

            self.mic_manager = MicStateManager(self)

            if self.mic_manager.start():
                self.log.info("✅ Gestionnaire micro Dragon démarré")
            else:
                self.log.warning("⚠️ Impossible de démarrer le gestionnaire micro")

            # Final splash update
            if self.splash and hasattr(self.splash, "update_progress"):
                self.splash.update_progress("Terminé!", 100)

            # Brief pause to show completion
            wx.CallLater(500, self.complete_startup)

        except Exception as e:
            self.log.error(f"Erreur lors de la finalisation: {e}")
            # Hide splash even on error
            if self.splash:
                self.splash.Close()

    def complete_startup(self):
        """Complete the startup sequence and hide splash."""
        try:
            from core import LOADED

            # Close splash screen
            if self.splash:
                self.splash.allow_close()  # Allow closing now
                self.splash.Close()
                self.splash = None

            # Log completion
            self.log.info("Application démarrée en mode tray")

            # Show status message briefly
            if self.tbicon:
                if LOADED:
                    grammar_count = len(LOADED)
                    message = f"FTNatlink démarré avec {grammar_count} grammaire(s)"
                else:
                    message = "FTNatlink démarré (aucune grammaire chargée)"

                # Show balloon tooltip if available
                try:
                    self.tbicon.ShowBalloon("FTNatlink", message, 3000)
                except:
                    # If balloon not supported, log the message
                    self.log.info(message)

        except Exception as e:
            self.log.error(f"Erreur lors de la completion du démarrage: {e}")

    def stop_background_task(self):
        """Stop any background tasks."""
        # Arrêter le gestionnaire de micro
        if self.mic_manager:
            self.log.info("Arrêt du gestionnaire micro Dragon")
            self.mic_manager.stop()
            self.mic_manager = None

        # Nettoyer le verrou d'instance
        if self.instance_manager:
            self.log.info("Nettoyage verrou d'instance")
            self.instance_manager.release_lock()
            self.instance_manager = None


def main():
    """Launch the tray application with splash screen"""
    try:
        # Create TrayApp directly - it will handle splash screen and single instance check
        app = TrayApp()
        app.MainLoop()

        # Clean up instance lock if it exists
        if hasattr(app, "instance_manager") and app.instance_manager:
            app.instance_manager.release_lock()

    except Exception as e:
        # Log error after app is created (to avoid delaying splash)
        try:
            self.log.error(f"Erreur critique dans main(): {e}")
        except:
            print(f"Critical error in main(): {e}")

        # Ensure cleanup even on error
        try:
            if hasattr(app, "instance_manager") and app.instance_manager:
                app.instance_manager.release_lock()
        except:
            pass

        # Clean up instance lock if it exists
        if hasattr(app, "instance_manager") and app.instance_manager:
            app.instance_manager.release_lock()

    except Exception as e:
        # Log error after app is created (to avoid delaying splash)
        try:
            self.log.error(f"Erreur critique dans main(): {e}")
        except:
            print(f"Critical error in main(): {e}")

        # Ensure cleanup even on error
        try:
            if hasattr(app, "instance_manager") and app.instance_manager:
                app.instance_manager.release_lock()
        except:
            pass


class TaskBarIcon(wx.adv.TaskBarIcon):
    """System tray icon with menu actions."""

    def __init__(self, frame):
        super(TaskBarIcon, self).__init__()
        self.frame = frame
        self.grammar_window = None  # Store reference to grammar window
        self.set_icon()

        # Bind events
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)

    @property
    def log(self):
        """Get logger from the main app"""
        try:
            app = wx.GetApp()
            if hasattr(app, "log"):
                return app.log
            else:
                # Fallback to basic logging
                from core.logHandler import log

                return log
        except Exception:
            # Last resort fallback
            import logging

            return logging.getLogger(__name__)

    def CreatePopupMenu(self):
        """Create right-click menu."""
        menu = wx.Menu()

        # Ajouter l'état du micro Dragon en premier
        app = wx.GetApp()
        if hasattr(app, "mic_manager") and app.mic_manager:
            if app.mic_manager.is_mic_on():
                menu.Append(0, "🎤 Micro Dragon: ON")
            else:
                menu.Append(0, "🔇 Micro Dragon: OFF")
            menu.Enable(0, False)  # Disable pour affichage seulement
            menu.AppendSeparator()

        menu.Append(1, "Show Status")
        menu.Append(2, "GUI Grammar Manager")
        menu.Append(3, "Reload Grammars")
        menu.AppendSeparator()
        menu.Append(4, "Restart")
        menu.Append(5, "Quit")

        self.Bind(wx.EVT_MENU, self.on_menu_item, id=1)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=2)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=3)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=4)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=5)
        return menu

    def set_icon(self):
        """Use your custom FTNATLINK icon."""
        img = wx.Image(ICON_PATH, wx.BITMAP_TYPE_ANY)
        img = img.Scale(32, 32, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(img)
        icon = wx.Icon()
        icon.CopyFromBitmap(bmp)
        self.SetIcon(icon, "FTNatLink")

    def on_left_click(self, event):
        """Left-click shows the same menu."""
        self.PopupMenu(self.CreatePopupMenu())

    def on_menu_item(self, event):
        """Handle menu item actions."""
        eid = event.GetId()

        if eid == 1:
            self.show_status()
        elif eid == 2:
            self.open_grammar_manager()
        elif eid == 3:
            self.reload_grammars()
        elif eid == 4:
            self.restart_app()
        elif eid == 5:
            self.quit_app()

    def open_grammar_manager(self):
        """Open or show the grammar manager window."""
        from core import LOADED
        from gui.main_frame import GrammarManagerFrame
        from pathlib import Path

        if self.grammar_window is None or not self.grammar_window:
            # Create new window
            self.grammar_window = GrammarManagerFrame()

            # Display already loaded grammars (loaded on startup)
            self.grammar_window.log_msg("� Grammar Manager - Current Status:")

            # Log loaded grammars
            if LOADED:
                for name, module in LOADED.items():
                    # Try to get addon info
                    addon_name = getattr(module, "__file__", "")
                    if addon_name:
                        addon_path = Path(addon_name).parent.name
                        self.grammar_window.log_msg(
                            f"Active grammar: {name} ({addon_path})"
                        )
                    else:
                        self.grammar_window.log_msg(f"Active grammar: {name}")
                self.grammar_window.log_msg(f"Total active grammars: {len(LOADED)}")
            else:
                self.grammar_window.log_msg("No grammars currently active")

            self.grammar_window.log_msg("")

            # Bind close event to hide instead of destroy
            self.grammar_window.Bind(wx.EVT_CLOSE, self.on_grammar_window_close)

        # Show the window
        self.grammar_window.Show()
        self.grammar_window.Raise()

    def on_grammar_window_close(self, event):
        """Handle grammar window close - hide instead of destroy."""
        self.grammar_window.Hide()

    def show_status(self):
        """Show current application status."""
        from core import LOADED

        if LOADED:
            grammar_list = "\n".join([f"• {name}" for name in LOADED.keys()])
            message = f"FTNatlink is running in background.\n\nLoaded grammars ({len(LOADED)}):\n{grammar_list}"
        else:
            message = (
                "FTNatlink is running in background.\n\nNo grammars currently loaded."
            )

        wx.MessageBox(message, "FTNatlink Status", wx.OK | wx.ICON_INFORMATION)

    def reload_grammars(self):
        """Reload all grammars."""
        try:
            from core.grammar_loader import load_grammars
            from core import LOADED

            self.log.info("Reloading grammars...")

            # Clear existing grammars first
            LOADED.clear()

            # Reload grammars
            load_grammars()

            # Log results
            if LOADED:
                for name, module in LOADED.items():
                    addon_name = getattr(module, "__file__", "")
                    if addon_name:
                        addon_path = Path(addon_name).parent.name
                        self.log.info(f"Reloaded grammar: {name} ({addon_path})")
                    else:
                        self.log.info(f"Reloaded grammar: {name}")
                self.log.info(f"Total grammars reloaded: {len(LOADED)}")

                wx.MessageBox(
                    f"Successfully reloaded {len(LOADED)} grammar(s)!",
                    "Reload Complete",
                    wx.OK | wx.ICON_INFORMATION,
                )
            else:
                self.log.warning("No grammars found after reload")
                wx.MessageBox(
                    "No grammars found to load.",
                    "Reload Complete",
                    wx.OK | wx.ICON_WARNING,
                )

        except Exception as e:
            self.log.error(f"Error reloading grammars: {e}")
            wx.MessageBox(
                f"Error reloading grammars:\n{e}", "Reload Error", wx.OK | wx.ICON_ERROR
            )

    def restart_app(self):
        """Restart the app properly by cleaning up current instance first."""
        try:
            self.log.info("Restarting application...")

            # Stop background thread first
            app = wx.GetApp()
            if hasattr(app, "stop_background_task"):
                app.stop_background_task()

            # Clean up grammar window if it exists
            if self.grammar_window:
                self.grammar_window.Destroy()
                self.grammar_window = None

            # Clean up tray icon
            self.Destroy()

            # Schedule the restart after cleanup
            wx.CallAfter(self._perform_restart)

        except Exception as e:
            self.log.error(f"Error during restart cleanup: {e}")
            self._perform_restart()

    def _perform_restart(self):
        """Perform the actual restart after cleanup."""
        try:
            # Close the current app frame
            if hasattr(self, "frame") and self.frame:
                self.frame.Close()

            # Start new instance
            python = sys.executable
            subprocess.Popen([python] + sys.argv)

            # Exit current process
            wx.GetApp().ExitMainLoop()

            # Force exit if MainLoop doesn't work
            wx.CallLater(2000, lambda: os._exit(0))

        except Exception as e:
            self.log.error(f"Error during restart: {e}")
            os._exit(0)

    def quit_app(self):
        """Properly quit the application with cleanup."""
        try:
            self.log.info("Quitting application...")

            # Stop background thread first
            app = wx.GetApp()
            if hasattr(app, "stop_background_task"):
                app.stop_background_task()

            # Clean up grammar window if it exists
            if self.grammar_window:
                self.grammar_window.Destroy()
                self.grammar_window = None

            # Clean up tray icon
            self.Destroy()

            # Close main frame
            if hasattr(self, "frame") and self.frame:
                self.frame.Close()

            # Exit the application
            wx.CallAfter(self._force_exit)

        except Exception as e:
            self.log.error(f"Error during quit: {e}")
            # Force exit if cleanup fails
            wx.CallAfter(self._force_exit)

    def _force_exit(self):
        """Force application exit."""
        try:
            wx.GetApp().ExitMainLoop()
        except:
            pass

        # As a last resort, force exit the process
        wx.CallLater(1000, lambda: os._exit(0))


# Note: L'ancienne classe MainApp (tray application) a été remplacée
# par l'utilisation de gui.app.NatlinkApp qui inclut l'écran de démarrage
# et une interface plus complète

if __name__ == "__main__":
    main()
