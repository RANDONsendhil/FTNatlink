"""
Module de vérification Dragon NaturallySpeaking
Vérifie que Dragon est disponible et fonctionnel avant de continuer
"""

import sys
import platform
import subprocess
import wx
from .logHandler import log
from .dragon_config import (
    FORCE_DRAGON_ONLY,
    ALLOW_MOCK_MODE,
    EXIT_ON_DRAGON_FAIL,
    DRAGON_NOT_FOUND_MESSAGE,
    PYTHON_64BIT_ERROR,
    NATLINK_CONNECTION_ERROR,
)


class DragonVerificationError(Exception):
    """Exception levée quand Dragon n'est pas disponible"""

    pass


def check_python_architecture():
    """Vérifie que Python est en 32-bit (requis pour Dragon)"""
    architecture = platform.architecture()[0]
    machine = platform.machine()

    # Check Python interpreter architecture, not machine architecture
    is_python_64bit = "64" in architecture

    log.info(f"Architecture Python: {architecture}")
    log.info(f"Machine: {machine}")
    log.info(f"Python 64-bit: {is_python_64bit}")

    if is_python_64bit:
        return False, f"Python {architecture} détecté (Dragon nécessite 32-bit)"

    return True, "Python 32-bit OK"


def check_dragon_process():
    """Vérifie si Dragon NaturallySpeaking est en cours d'exécution"""
    dragon_processes = ["natspeak.exe", "dragon.exe", "dragonbar.exe", "dgnuiasvr.exe"]

    running_processes = []

    try:
        # Vérifier les processus Dragon
        for process_name in dragon_processes:
            try:
                result = subprocess.run(
                    ["tasklist", "/fi", f"imagename eq {process_name}"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if process_name.lower() in result.stdout.lower():
                    running_processes.append(process_name)
            except Exception as e:
                log.warning(
                    f"Erreur lors de la vérification du processus {process_name}: {e}"
                )

        if running_processes:
            log.info(f"Processus Dragon détectés: {running_processes}")
            return True, f"Dragon en cours d'exécution: {', '.join(running_processes)}"
        else:
            log.warning("Aucun processus Dragon détecté")
            return False, "Aucun processus Dragon NaturallySpeaking trouvé"

    except Exception as e:
        log.error(f"Erreur lors de la vérification des processus: {e}")
        return False, f"Erreur de vérification: {e}"


def check_natlink_availability():
    """Vérifie si natlink est disponible et fonctionnel"""
    try:
        import natlink

        log.info("Module natlink importé avec succès")

        # Vérifier si Dragon est en cours d'exécution selon natlink
        try:
            is_running = natlink.isNatSpeakRunning()
            log.info(f"Dragon en cours selon natlink: {is_running}")

            if not is_running:
                return False, "Dragon NaturallySpeaking n'est pas démarré selon natlink"

            # Simple test - if isNatSpeakRunning works, natlink is functional
            log.info("Test de natlink basique réussi")
            return True, "Natlink opérationnel"

        except Exception as e:
            log.error(f"Erreur lors de la vérification de l'état Dragon: {e}")
            return False, f"Erreur natlink: {e}"

    except ImportError as e:
        log.error(f"Module natlink non disponible: {e}")
        return False, f"Natlink non installé: {e}"
    except Exception as e:
        log.error(f"Erreur natlink inattendue: {e}")
        return False, f"Erreur natlink: {e}"


def check_dragon_mic_state():
    """Vérifie l'état du micro Dragon (ON/OFF)"""
    log.info("[DEBUG] check_dragon_mic_state() called")
    try:
        import natlink

        # Vérifier si Dragon est en cours d'exécution
        if not natlink.isNatSpeakRunning():
            log.info("[DEBUG] natlink.isNatSpeakRunning() returned False")
            return False, "Dragon NaturallySpeaking n'est pas en cours d'exécution"

        # Se connecter à Dragon avant de vérifier le micro
        try:
            natlink.natConnect()
            log.info("[DEBUG] natConnect() successful")
        except Exception as e:
            log.error(f"Erreur natConnect(): {e}")
            return False, f"Impossible de se connecter à Dragon: {e}"

        # Vérifier l'état du micro
        try:
            mic_state = natlink.getMicState()
            log.info(f"[DEBUG] natlink.getMicState() returned: {mic_state}")
            log.info(f"État micro Dragon: {mic_state}")

            if mic_state == "on":
                log.info(" -------------------------------> [DEBUG] Micro is ON")
                return True, "Micro Dragon activé"
            elif mic_state == "off":
                log.info(" -------------------------------> [DEBUG] Micro is OFF")
                return False, "Micro Dragon éteint"
            elif mic_state == "sleeping":
                log.info(" -------------------------------> [DEBUG] Micro is SLEEPING")
                return False, "Micro Dragon en veille"
            elif mic_state == "disabled":
                log.info(" -------------------------------> [DEBUG] Micro is DISABLED")
                return False, "Micro Dragon désactivé"
            else:
                log.info(f"[DEBUG] Micro unknown state: {mic_state}")
                return False, f"État micro inconnu: {mic_state}"

        except AttributeError:
            # Si getMicState n'existe pas, on assume que Dragon est opérationnel
            log.warning("getMicState non disponible - on assume micro actif")
            return True, "État micro non vérifiable (assumé actif)"

        except Exception as e:
            log.error(f"Erreur lors de la vérification état micro: {e}")
            return False, f"Erreur vérification micro: {e}"

    except ImportError:
        return False, "Natlink non disponible pour vérifier le micro"
    except Exception as e:
        log.error(f"Erreur lors de la vérification micro Dragon: {e}")
        return False, f"Erreur micro: {e}"


def verify_dragon_availability():
    """
    Vérifie complètement que Dragon est disponible et fonctionnel
    Retourne (success: bool, message: str)
    """
    log.info("🔍 Vérification de Dragon NaturallySpeaking...")

    # 1. Vérifier l'architecture Python
    python_ok, python_msg = check_python_architecture()
    if not python_ok:
        log.error(f"❌ Architecture Python: {python_msg}")
        return False, PYTHON_64BIT_ERROR
    else:
        log.info(f"✅ Architecture Python: {python_msg}")

    # 2. Vérifier les processus Dragon
    process_ok, process_msg = check_dragon_process()
    if not process_ok:
        log.error(f"❌ Processus Dragon: {process_msg}")
        return False, DRAGON_NOT_FOUND_MESSAGE
    else:
        log.info(f"✅ Processus Dragon: {process_msg}")

    # 3. Vérifier natlink
    natlink_ok, natlink_msg = check_natlink_availability()
    if not natlink_ok:
        log.error(f"❌ Natlink: {natlink_msg}")
        return False, NATLINK_CONNECTION_ERROR
    else:
        log.info(f"✅ Natlink: {natlink_msg}")

    # 4. Vérifier l'état du micro Dragon (si requis)
    from .dragon_config import REQUIRE_MIC_ON, DRAGON_MIC_OFF_ERROR

    if REQUIRE_MIC_ON:
        mic_ok, mic_msg = check_dragon_mic_state()
        if not mic_ok:
            log.error(f"❌ Micro Dragon: {mic_msg}")
            return False, DRAGON_MIC_OFF_ERROR
        else:
            log.info(f"✅ Micro Dragon: {mic_msg}")

    log.info("🎉 Dragon NaturallySpeaking est disponible et opérationnel!")
    return True, "Dragon NaturallySpeaking opérationnel"


def enforce_dragon_requirement():
    """
    Force l'exigence de Dragon selon la configuration
    Lève une exception ou affiche une erreur si Dragon n'est pas disponible
    """
    if not FORCE_DRAGON_ONLY:
        log.info("Mode Dragon forcé désactivé - mode mixte autorisé")
        return True

    log.info("🛡️ Mode Dragon UNIQUEMENT activé - vérification obligatoire...")

    # Vérifier Dragon
    success, message = verify_dragon_availability()

    log.info(
        f"[DEBUG] enforce_dragon_requirement: verify_dragon_availability() returned: {success}, {message}"
    )

    if not success:
        log.error("❌ Dragon NaturallySpeaking requis mais non disponible")

        if EXIT_ON_DRAGON_FAIL:
            log.info("[DEBUG] EXIT_ON_DRAGON_FAIL is True, will show error and exit.")
            # Afficher l'erreur à l'utilisateur
            try:
                app = wx.GetApp()
                if app is None:
                    # Créer une app temporaire pour le message d'erreur
                    app = wx.App()

                wx.MessageBox(
                    message, "Dragon NaturallySpeaking Requis", wx.OK | wx.ICON_ERROR
                )
            except Exception as e:
                log.error(f"Erreur lors de l'affichage du message: {e}")
                print(message)  # Fallback vers la console

            # Quitter l'application
            log.error("Application fermée - Dragon NaturallySpeaking requis")
            log.info("[DEBUG] Raising DragonVerificationError to exit app.")
            raise DragonVerificationError(message)
        else:
            log.warning("Dragon non disponible mais EXIT_ON_DRAGON_FAIL=False")
            return False

    log.info("✅ Vérification Dragon réussie - application peut continuer")
    return True
