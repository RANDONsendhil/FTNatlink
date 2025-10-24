"""
Moniteur d'état du micro Dragon NaturallySpeaking
Surveille en continu l'état du micro Dragon et gère l'activation/désactivation de FTNatlink
"""

import threading
import time
import wx
from .logHandler import log
from .dragon_config import REQUIRE_MIC_ON, DRAGON_MIC_OFF_ERROR


class MicEventHandler:
    """Event handler for Dragon microphone state changes using natlink.MacroSystem"""

    def __init__(self):
        self.mic_state = "unknown"
        self.listeners = []  # Callbacks pour les changements d'état
        self.macro_system = None
        self._setup_event_handler()

    def _setup_event_handler(self):
        """Setup natlink callbacks for mic event handling"""
        try:
            import natlink

            # Connect to natlink
            if not hasattr(self, "connected"):
                self.connected = False

            if not self.connected:
                try:
                    natlink.natConnect()
                    self.connected = True
                    log.info("✅ MicEventHandler connected to natlink")
                except Exception as e:
                    log.debug(f"natConnect in MicEventHandler: {e}")
                    self.connected = True  # Assume connected

            # Get initial mic state
            try:
                self.mic_state = natlink.getMicState()
                log.info(f"Initial mic state: {self.mic_state}")
            except Exception as e:
                log.debug(f"Could not get initial mic state: {e}")
                self.mic_state = "unknown"

            log.info("✅ MicEventHandler setup complete")
            return True

        except Exception as e:
            log.error(f"Failed to setup MicEventHandler: {e}")
            return False

    def add_listener(self, callback):
        """Add a callback for mic state changes"""
        self.listeners.append(callback)

    def get_current_mic_state(self):
        """Get current microphone state"""
        # Try to get fresh state from natlink
        try:
            import natlink

            if hasattr(self, "connected") and self.connected:
                current_state = natlink.getMicState()
                if current_state != self.mic_state:
                    # State changed, update and notify
                    old_state = self.mic_state
                    self.mic_state = current_state
                    for listener in self.listeners:
                        try:
                            listener(old_state, current_state)
                        except Exception as e:
                            log.error(f"Error in mic state listener: {e}")
                return current_state
        except Exception as e:
            log.debug(f"Could not get fresh mic state: {e}")

        return self.mic_state

    def is_mic_on(self):
        """Return True if microphone is on"""
        current_state = self.get_current_mic_state()
        return current_state == "on"


class DragonMicMonitor:
    """Moniteur qui surveille l'état du micro Dragon en continu."""

    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.mic_state = False
        self.listeners = []  # Callbacks pour les changements d'état
        self.natlink = None
        self.connected = False  # Track if natConnect has been called

    def start_monitoring(self):
        """Démarre la surveillance du micro Dragon."""
        if self.monitoring:
            log.warning("Surveillance micro Dragon déjà active")
            return

        log.info("🎤 Démarrage surveillance micro Dragon")
        self.monitoring = True

        # Tenter d'importer natlink et vérifier les fonctions requises
        try:
            import natlink

            self.natlink = natlink

            # Vérifier si les fonctions natlink requises sont disponibles
            if not hasattr(natlink, "isNatSpeakRunning"):
                log.warning(
                    "❌ isNatSpeakRunning non disponible - surveillance micro désactivée"
                )
                return False

            if not hasattr(natlink, "getMicState"):
                log.warning(
                    "❌ getMicState non disponible - surveillance micro désactivée"
                )
                return False

            # Faire une connexion initiale ici dans le thread principal
            try:
                if hasattr(natlink, "natConnect"):
                    natlink.natConnect()
                    self.connected = True
                    log.info("✓ Initial natConnect() for monitoring")
            except Exception as e:
                log.debug(f"Initial natConnect warning: {e}")
                self.connected = True  # Assume connected

            log.info("✅ Natlink disponible pour surveillance micro")
        except ImportError:
            log.error("❌ Natlink non disponible - surveillance micro impossible")
            return False

        # Démarrer le thread de surveillance
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        return True

    def stop_monitoring(self):
        """Arrête la surveillance du micro Dragon."""
        log.info("🔴 Arrêt surveillance micro Dragon")
        self.monitoring = False

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)

    def add_listener(self, callback):
        """Ajoute un callback qui sera appelé lors des changements d'état du micro."""
        self.listeners.append(callback)

    def remove_listener(self, callback):
        """Retire un callback de la liste."""
        if callback in self.listeners:
            self.listeners.remove(callback)

    def _monitor_loop(self):
        """Boucle principale de surveillance du micro."""
        log.info("📡 Boucle surveillance micro démarrée")

        while self.monitoring:
            try:
                # Vérifier l'état du micro
                new_mic_state = self._check_mic_state()

                # Si l'état a changé, notifier les listeners
                if new_mic_state != self.mic_state:
                    old_state = self.mic_state
                    self.mic_state = new_mic_state

                    log.info(f"🎤 Micro Dragon: {'ON' if new_mic_state else 'OFF'}")

                    # Notifier tous les listeners
                    for listener in self.listeners:
                        try:
                            wx.CallAfter(listener, new_mic_state, old_state)
                        except Exception as e:
                            log.error(f"Erreur lors de la notification listener: {e}")

                # Attendre avant la prochaine vérification
                time.sleep(1)  # Vérifier chaque seconde

            except Exception as e:
                log.error(f"Erreur dans la surveillance micro: {e}")
                # Stop monitoring on repeated errors to prevent loops
                log.error("Arrêt de la surveillance micro en raison d'erreurs répétées")
                self.monitoring = False
                break

        log.info("📡 Boucle surveillance micro arrêtée")

    def _check_mic_state(self):
        """Vérifie l'état actuel du micro Dragon."""
        if not self.natlink:
            return False

        try:
            # Vérifier si les fonctions natlink sont disponibles
            if not hasattr(self.natlink, "isNatSpeakRunning"):
                return False

            # Vérifier si Dragon est en cours d'exécution
            if not self.natlink.isNatSpeakRunning():
                self.connected = False
                return False

            # Se connecter à Dragon si nécessaire (une seule fois)
            if not self.connected:
                try:
                    if hasattr(self.natlink, "natConnect"):
                        self.natlink.natConnect()
                        self.connected = True
                        log.info("✓ natConnect() successful (mic monitor)")
                except Exception as e:
                    # natConnect peut échouer si déjà connecté dans un autre contexte
                    # On essaye de continuer quand même
                    log.debug(f"natConnect in monitor: {e}")
                    self.connected = True  # Assume it's connected

            # Vérifier l'état du micro via natlink
            # getMicState() retourne généralement:
            # - 'on' : micro activé
            # - 'off' : micro éteint
            # - 'sleeping' : en veille
            # - 'disabled' : désactivé
            if hasattr(self.natlink, "getMicState"):
                try:
                    mic_state = self.natlink.getMicState()
                    return mic_state == "on"
                except Exception as e:
                    # Si getMicState échoue (COM error), on assume que le micro est ON
                    # puisque Dragon fonctionne et les grammaires sont actives
                    if "0x800401f0" in str(e) or "CO_E_NOTINITIALIZED" in str(e):
                        log.debug(f"COM error getting mic state, assuming ON: {e}")
                        return True
                    else:
                        log.error(f"Erreur getMicState: {e}")
                        return False
            else:
                # Si getMicState n'existe pas, assume que Dragon est opérationnel
                return True

        except Exception as e:
            log.error(f"Erreur lors de la vérification micro: {e}")
            self.connected = False
            return False

    def get_current_mic_state(self):
        """Retourne l'état actuel du micro (True si ON, False si OFF)."""
        return self.mic_state

    def force_check(self):
        """Force une vérification immédiate de l'état du micro."""
        if not self.monitoring:
            return self._check_mic_state()
        return self.mic_state


class MicStateManager:
    """Gestionnaire qui contrôle FTNatlink selon l'état du micro Dragon."""

    def __init__(self, app_controller):
        self.app_controller = app_controller  # Référence vers l'app principale
        self.mic_handler = (
            MicEventHandler()
        )  # Use event handler instead of polling monitor
        self.grammars_active = False
        self.waiting_for_mic = False

        # Écouter les changements d'état du micro
        self.mic_handler.add_listener(self.on_mic_state_changed)

    def start(self):
        """Démarre la gestion de l'état du micro."""
        log.info(f"DEBUG: REQUIRE_MIC_ON = {REQUIRE_MIC_ON}")
        if not REQUIRE_MIC_ON:
            log.info("Surveillance micro désactivée par configuration")
            return True

        # Check if natlink functions are available before starting monitoring
        try:
            import natlink

            if not hasattr(natlink, "isNatSpeakRunning"):
                log.warning(
                    "⚠️ Natlink functions not available - disabling mic monitoring"
                )
                return True
        except ImportError:
            log.warning("⚠️ Natlink not available - disabling mic monitoring")
            return True

        log.info("🎤 Démarrage gestionnaire état micro Dragon avec MicEventHandler")

        # Get initial mic state
        initial_state = self.mic_handler.get_current_mic_state()
        log.info(f"État initial micro Dragon: {initial_state}")

        if initial_state != "on":
            self._handle_mic_off()
        else:
            self._handle_mic_on()

        return True

    def stop(self):
        """Arrête la gestion de l'état du micro."""
        log.info("🔴 Arrêt gestionnaire état micro")
        # No need to stop anything as event handler is automatic

    def on_mic_state_changed(self, old_state, new_state):
        """Callback appelé lors du changement d'état du micro Dragon."""
        log.info(f"🎤 Micro Dragon state change: {old_state} → {new_state}")

        # Update tray icon if available
        self._update_tray_menu()

        if new_state == "on":
            self._handle_mic_on()
        else:
            self._handle_mic_off()

    def _update_tray_menu(self):
        """Update the tray menu to reflect current mic state"""
        try:
            app = self.app_controller
            if hasattr(app, "tbicon") and app.tbicon:
                # Force the tray menu to refresh by triggering a menu recreate
                # This will happen automatically next time the user opens the menu
                pass
        except Exception as e:
            log.error(f"Error updating tray menu: {e}")

    def _handle_mic_on(self):
        """Gérer l'activation du micro Dragon."""
        log.info("🟢 Micro Dragon activé - activation des grammaires")

        if self.waiting_for_mic:
            self.waiting_for_mic = False
            # Afficher notification de reprise
            try:
                if (
                    hasattr(self.app_controller, "tbicon")
                    and self.app_controller.tbicon
                ):
                    self.app_controller.tbicon.ShowBalloon(
                        "FTNatlink", "Micro Dragon activé - FTNatlink actif", 3000
                    )
            except:
                pass

        # Activer les grammaires si pas déjà fait
        if not self.grammars_active:
            self._activate_grammars()

    def _handle_mic_off(self):
        """Gérer la désactivation du micro Dragon."""
        log.info("🔴 Micro Dragon désactivé - pause des grammaires")

        if not self.waiting_for_mic:
            self.waiting_for_mic = True

            # Afficher notification d'attente
            try:
                if (
                    hasattr(self.app_controller, "tbicon")
                    and self.app_controller.tbicon
                ):
                    self.app_controller.tbicon.ShowBalloon(
                        "FTNatlink", "Micro Dragon éteint - FTNatlink en pause", 3000
                    )
            except:
                pass

        # Désactiver les grammaires
        if self.grammars_active:
            self._deactivate_grammars()

    def _activate_grammars(self):
        """Active les grammaires FTNatlink."""
        try:
            # Réactiver les grammaires chargées
            from core import LOADED

            for name, module in LOADED.items():
                if hasattr(module, "load") and callable(module.load):
                    module.load()
                    log.info(f"Grammaire réactivée: {name}")

            self.grammars_active = True
            log.info(f"✅ {len(LOADED)} grammaire(s) activée(s)")

        except Exception as e:
            log.error(f"Erreur lors de l'activation des grammaires: {e}")

    def _deactivate_grammars(self):
        """Désactive les grammaires FTNatlink."""
        try:
            # Désactiver les grammaires chargées
            from core import LOADED

            for name, module in LOADED.items():
                if hasattr(module, "unload") and callable(module.unload):
                    module.unload()
                    log.info(f"Grammaire désactivée: {name}")

            self.grammars_active = False
            log.info(f"⏸️ {len(LOADED)} grammaire(s) désactivée(s)")

        except Exception as e:
            log.error(f"Erreur lors de la désactivation des grammaires: {e}")

    def is_mic_on(self):
        """Retourne True si le micro Dragon est activé."""
        return self.mic_handler.is_mic_on()

    def is_grammars_active(self):
        """Retourne True si les grammaires sont actives."""
        return self.grammars_active
