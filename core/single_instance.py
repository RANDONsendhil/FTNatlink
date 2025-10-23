"""
Gestionnaire d'instance unique pour FTNatlink (SANS DÉPENDANCES EXTERNES)
Empêche le lancement de plusieurs instances simultanées
Utilise uniquement les fonctions Windows intégrées
"""

import os
import sys
import tempfile
import subprocess
import time
import wx
import psutil
from pathlib import Path
from .logHandler import log


class SingleInstanceManager:
    """Gestionnaire pour s'assurer qu'une seule instance de FTNatlink fonctionne."""

    def __init__(self, app_name="FTNatlink"):
        self.app_name = app_name
        self.lock_file = None
        self.lock_file_path = None
        self.pid = os.getpid()

    def is_already_running(self):
        """Vérifie si une autre instance de FTNatlink est déjà en cours d'exécution."""
        try:
            # Méthode 1: Utiliser psutil si disponible (plus fiable)
            running_pid = self._check_processes_psutil()
            if running_pid:
                log.info(f"Instance FTNatlink détectée via psutil: PID {running_pid}")
                return True, running_pid

            # Méthode 2: Vérifier les processus via tasklist (fallback Windows)
            running_pid = self._check_processes_tasklist()
            if running_pid:
                log.info(f"Instance FTNatlink détectée via tasklist: PID {running_pid}")
                return True, running_pid

            # Méthode 3: Vérifier le fichier de verrouillage
            return self._check_lock_file()

        except Exception as e:
            log.error(f"Erreur lors de la vérification d'instance: {e}")
            # En cas d'erreur, utiliser uniquement le fichier de verrouillage
            return self._check_lock_file()

    def _check_processes_psutil(self):
        """Vérifier les processus FTNatlink en utilisant psutil."""
        try:
            for process in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    info = process.info
                    pid = info.get("pid")
                    name = (info.get("name") or "").lower()
                    cmdline = info.get("cmdline") or []

                    # Skip current process
                    if pid == self.pid:
                        continue

                    # Direct exe match
                    if name == "ftnatlink.exe" or name == "ftnatlink":
                        return pid

                    # Python process running __init__.py inside FTNatlink
                    try:
                        if name == "python.exe" or name == "python":
                            joined = " ".join(map(str, cmdline)).lower()
                            # More specific check: must be running __init__.py from FTNatlink folder
                            # and NOT be VS Code extensions or other tools
                            if (
                                "__init__.py" in joined
                                and "ftnatlink" in joined
                                and "ftnatlink\\__init__.py" in joined
                                and "vscode" not in joined
                                and "lsp_server" not in joined
                            ):
                                return pid
                    except Exception:
                        pass

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue

        except Exception as e:
            log.warning(f"psutil check error: {e}")

        return None

    def _check_processes_tasklist(self):
        """Vérifier les processus FTNatlink via tasklist (Windows natif)."""
        try:
            # Chercher FTNatlink.exe
            result = subprocess.run(
                ["tasklist", "/fi", "imagename eq FTNatlink.exe", "/fo", "csv"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0 and "FTNatlink.exe" in result.stdout:
                lines = result.stdout.strip().split("\n")
                for line in lines[1:]:  # Skip header
                    if "FTNatlink.exe" in line:
                        # Extraire le PID (format CSV: "nom","pid",...)
                        parts = line.split(",")
                        if len(parts) >= 2:
                            try:
                                pid = int(parts[1].strip('"'))
                                if pid != self.pid:  # Pas notre propre processus
                                    return pid
                            except ValueError:
                                continue

            # Chercher aussi python.exe avec __init__.py
            result = subprocess.run(
                [
                    "wmic",
                    "process",
                    "where",
                    'name="python.exe"',
                    "get",
                    "processid,commandline",
                    "/format:csv",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines[1:]:  # Skip header
                    if "__init__.py" in line and "FTNatlink" in line:
                        # Extraire le PID
                        parts = line.split(",")
                        try:
                            pid = int(parts[-1].strip())
                            if pid != self.pid:  # Pas notre propre processus
                                return pid
                        except (ValueError, IndexError):
                            continue

            return None

        except Exception as e:
            log.warning(f"Erreur lors de la vérification tasklist: {e}")
            return None

        except Exception as e:
            log.error(f"Erreur lors de la vérification d'instance: {e}")
            return False, None

    def _check_lock_file(self):
        """Vérifie le fichier de verrouillage."""
        try:
            # Créer le chemin du fichier de verrouillage
            temp_dir = tempfile.gettempdir()
            self.lock_file_path = Path(temp_dir) / f"{self.app_name}.lock"

            if self.lock_file_path.exists():
                # Lire le PID du fichier de verrouillage
                try:
                    with open(self.lock_file_path, "r") as f:
                        stored_pid = int(f.read().strip())

                    # Vérifier si le processus avec ce PID existe encore (Windows natif)
                    if self._pid_exists_windows(stored_pid):
                        log.info(f"Fichier verrou trouvé avec PID actif: {stored_pid}")
                        return True, stored_pid

                    # Le processus n'existe plus, supprimer le fichier obsolète
                    log.info("Suppression fichier verrou obsolète")
                    self.lock_file_path.unlink()

                except (ValueError, IOError) as e:
                    log.warning(f"Erreur lecture fichier verrou: {e}")
                    # Supprimer le fichier corrompu
                    try:
                        self.lock_file_path.unlink()
                    except:
                        pass

            return False, None

        except Exception as e:
            log.error(f"Erreur vérification fichier verrou: {e}")
            return False, None

    def _pid_exists_windows(self, pid):
        """Vérifie si un PID existe sous Windows (sans psutil)."""
        try:
            # Utiliser tasklist pour vérifier si le PID existe
            result = subprocess.run(
                ["tasklist", "/fi", f"pid eq {pid}", "/fo", "csv"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                # Si le PID existe, tasklist retourne des données
                lines = result.stdout.strip().split("\n")
                # More than one line means there are results (header + data)
                if len(lines) > 1:
                    # Verify the exact PID is in the output
                    for line in lines[1:]:  # Skip header
                        if line and str(pid) in line:
                            # Additional check: ensure it's the exact PID, not a substring
                            parts = line.split(",")
                            if len(parts) >= 2:
                                try:
                                    found_pid = int(parts[1].strip('"'))
                                    return found_pid == pid
                                except ValueError:
                                    continue
                return False

            return False

        except Exception as e:
            log.warning(f"Erreur lors de la vérification PID {pid}: {e}")
            return False

    def create_lock(self):
        """Crée le fichier de verrouillage pour cette instance."""
        try:
            if not self.lock_file_path:
                temp_dir = tempfile.gettempdir()
                self.lock_file_path = Path(temp_dir) / f"{self.app_name}.lock"

            # Écrire le PID dans le fichier de verrouillage
            with open(self.lock_file_path, "w") as f:
                f.write(str(self.pid))

            log.info(f"Fichier verrou créé: {self.lock_file_path} (PID: {self.pid})")
            return True

        except Exception as e:
            log.error(f"Erreur création fichier verrou: {e}")
            return False

    def release_lock(self):
        """Supprime le fichier de verrouillage."""
        try:
            if self.lock_file_path and self.lock_file_path.exists():
                self.lock_file_path.unlink()
                log.info("Fichier verrou supprimé")

        except Exception as e:
            log.error(f"Erreur suppression fichier verrou: {e}")

    def show_already_running_message(self, existing_pid=None):
        """Affiche un message indiquant que FTNatlink est déjà en cours d'exécution."""
        try:
            # Créer une application temporaire pour le message
            app = wx.App()

            message = "FTNatlink est déjà en cours d'exécution.\n\n"

            if existing_pid:
                message += f"Instance active (PID: {existing_pid})\n\n"

            message += "Actions possibles:\n"
            message += "• Vérifiez l'icône dans la barre des tâches\n"
            message += "• Utilisez le Gestionnaire des tâches pour fermer l'instance existante\n"
            message += "• Redémarrez votre ordinateur si nécessaire"

            wx.MessageBox(
                message, "FTNatlink - Instance déjà active", wx.OK | wx.ICON_WARNING
            )

            app.Destroy()

        except Exception as e:
            log.error(f"Erreur affichage message: {e}")
            # Fallback vers la console
            print("\n" + "=" * 50)
            print("❌ ERREUR: FTNatlink est déjà en cours d'exécution!")
            print("=" * 50)
            if existing_pid:
                print(f"Instance active (PID: {existing_pid})")
            print("Fermez l'instance existante avant de relancer.")
            print("=" * 50 + "\n")

    def force_close_existing_instances(self):
        """Force la fermeture des instances existantes (à utiliser avec précaution)."""
        try:
            closed_instances = []

            for process in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    info = process.info
                    pid = info.get("pid")
                    name = (info.get("name") or "").lower()
                    cmdline = info.get("cmdline") or []

                    # Skip current process
                    if pid == self.pid:
                        continue

                    # Check if it's FTNatlink
                    is_ftnatlink = False

                    # Direct exe match
                    if name == "ftnatlink.exe" or name == "ftnatlink":
                        is_ftnatlink = True

                    # Python process running __init__.py inside FTNatlink
                    elif name == "python.exe" or name == "python":
                        try:
                            joined = " ".join(map(str, cmdline)).lower()
                            if "__init__.py" in joined and "ftnatlink" in joined:
                                is_ftnatlink = True
                        except Exception:
                            pass

                    if is_ftnatlink:
                        log.info(f"Forcing close of FTNatlink instance: PID {pid}")

                        # Tenter fermeture propre d'abord
                        process.terminate()

                        # Attendre un peu
                        try:
                            process.wait(timeout=3)
                        except psutil.TimeoutExpired:
                            # Forcer la fermeture
                            log.warning(f"Force killing stubborn process: PID {pid}")
                            process.kill()

                        closed_instances.append(pid)
                        log.info(f"Instance fermée: PID {pid}")

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue

            return closed_instances

        except Exception as e:
            log.error(f"Erreur lors de la fermeture des instances: {e}")
            return []


def check_single_instance():
    """
    Fonction utilitaire pour vérifier et gérer l'instance unique.
    Retourne True si l'application peut continuer, False sinon.
    """
    manager = SingleInstanceManager()

    # Vérifier si une instance existe déjà
    already_running, existing_pid = manager.is_already_running()

    if already_running:
        log.warning(f"Instance FTNatlink déjà active (PID: {existing_pid})")

        # Afficher le message à l'utilisateur
        manager.show_already_running_message(existing_pid)

        # Ne pas continuer
        return False, manager

    # Créer le verrou pour cette instance
    if manager.create_lock():
        log.info("Instance unique confirmée - application peut continuer")
        return True, manager
    else:
        log.error("Impossible de créer le verrou d'instance")
        return False, manager
