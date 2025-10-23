"""
Moniteur d'état du micro Dragon NaturallySpeaking
Surveille en continu l'état du micro Dragon et gère l'activation/désactivation de FTNatlink
"""

import threading
import time
import wx
from .logHandler import log
from .dragon_config import REQUIRE_MIC_ON, DRAGON_MIC_OFF_ERROR


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
        self.monitor = DragonMicMonitor()
        self.grammars_active = False
        self.waiting_for_mic = False

        # Écouter les changements d'état du micro
        self.monitor.add_listener(self.on_mic_state_changed)

    def start(self):
        """Démarre la gestion de l'état du micro."""
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

        log.info("🎤 Démarrage gestionnaire état micro Dragon")

        # Démarrer la surveillance
        if not self.monitor.start_monitoring():
            log.error("Impossible de démarrer la surveillance micro")
            return False

        # Donner un peu de temps pour que la surveillance démarre et se connecte
        time.sleep(0.5)

        # Vérification initiale
        initial_state = self.monitor.force_check()
        log.info(f"État initial micro Dragon: {'ON' if initial_state else 'OFF'}")

        if not initial_state:
            self._handle_mic_off()
        else:
            self._handle_mic_on()

        return True

    def stop(self):
        """Arrête la gestion de l'état du micro."""
        log.info("🔴 Arrêt gestionnaire état micro")
        self.monitor.stop_monitoring()

    def on_mic_state_changed(self, new_state, old_state):
        """Callback appelé quand l'état du micro change."""
        if new_state:
            self._handle_mic_on()
        else:
            self._handle_mic_off()

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
        return self.monitor.get_current_mic_state()

    def is_grammars_active(self):
        """Retourne True si les grammaires sont actives."""
        return self.grammars_active
