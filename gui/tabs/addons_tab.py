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
from core.logHandler import log


def create_addons_tab(parent, frame):
    """Create the Addons installation tab"""
    panel = wx.Panel(parent)

    # Title
    title = wx.StaticText(panel, label="Gestion des Addons")
    title_font = title.GetFont()
    title_font.PointSize += 2
    title_font = title_font.Bold()
    title.SetFont(title_font)

    # Instructions
    instructions = wx.StaticText(
        panel,
        label="Installez des addons de commandes vocales depuis des fichiers .natlink-addon.\n\n"
        "Vous pouvez :\n"
        "• Installer des addons depuis votre ordinateur\n"
        "• Empaqueter vos propres addons\n"
        "• Partager des addons avec d'autres",
    )

    # Install button
    install_btn = wx.Button(panel, label="Installer un Addon depuis un Fichier")
    install_btn.SetFont(install_btn.GetFont().Bold())

    # Package button
    package_info = wx.StaticText(
        panel,
        label="\nPour créer des paquets d'addon :\n"
        "Utilisez : python addon_packager.py addons/votre_addon",
    )
    package_info.SetForegroundColour(wx.Colour(100, 100, 100))

    # Bind events
    install_btn.Bind(wx.EVT_BUTTON, lambda e: on_install(e, frame))

    # Layout
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(title, 0, wx.ALL, 10)
    sizer.Add(instructions, 0, wx.ALL | wx.EXPAND, 10)
    sizer.Add(install_btn, 0, wx.CENTER | wx.ALL, 20)
    sizer.Add(package_info, 0, wx.ALL, 10)
    sizer.AddStretchSpacer()

    panel.SetSizer(sizer)
    return panel


def on_install(event, frame):
    """Open file dialog to select and install an addon"""
    frame.log_msg("\nOuverture du navigateur de fichiers...")

    with wx.FileDialog(
        frame,
        "Sélectionner un Addon Natlink à Installer",
        wildcard="Addon Natlink (*.natlink-addon)|*.natlink-addon|Tous les fichiers (*.*)|*.*",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
    ) as dlg:
        if dlg.ShowModal() == wx.ID_CANCEL:
            frame.log_msg("Installation annulée par l'utilisateur")
            return

        addon_path = dlg.GetPath()
        frame.log_msg(f"Sélectionné : {Path(addon_path).name}")
        frame.log_msg("Installation de l'addon...")

        try:
            # Install the addon
            result = install_addon(addon_path)

            if result:
                frame.log_msg(
                    f"Addon installé avec succès : {result['name']} v{result['version']}"
                )
                frame.log_msg(f"Installé {result['files_installed']} fichiers Python")
            else:
                frame.log_msg("Addon installé avec succès !")

            # Reload grammars to activate new addon
            frame.log_msg("Rechargement des grammaires...")
            reload_grammars()
            frame.log_msg("Grammaires rechargées !")

            # Show success message
            success_msg = (
                f"Addon installé avec succès !\n\nFichier : {Path(addon_path).name}"
            )
            if result:
                success_msg += f"\nNom : {result['name']}\nVersion : {result['version']}\nFichiers : {result['files_installed']}"
            success_msg += "\n\nLes grammaires ont été rechargées."

            wx.MessageBox(
                success_msg, "Installation Terminée", wx.OK | wx.ICON_INFORMATION
            )

            # Refresh grammar list if the method exists
            if hasattr(frame, "grammar_list"):
                from core.grammar_loader import list_grammars

                grammars = list_grammars()
                frame.grammar_list.Clear()

                if grammars:
                    for g in grammars:
                        frame.grammar_list.Append(f"{g}")

        except FileNotFoundError as e:
            error_msg = f"Fichier non trouvé :\n{e}"
            frame.log_msg(f"{error_msg}")
            wx.MessageBox(error_msg, "Installation Échouée", wx.OK | wx.ICON_ERROR)

        except ValueError as e:
            error_msg = f"Invalid addon file:\n{e}"
            frame.log_msg(f"{error_msg}")
            wx.MessageBox(error_msg, "Invalid Addon", wx.OK | wx.ICON_ERROR)

        except zipfile.BadZipFile as e:
            error_msg = f"Corrupted addon file:\nThe selected file is not a valid zip archive or is corrupted."
            frame.log_msg(f"{error_msg}")
            wx.MessageBox(error_msg, "Corrupted File", wx.OK | wx.ICON_ERROR)

        except PermissionError as e:
            error_msg = f"Permission denied:\nUnable to install addon due to file permissions.\nTry running as administrator."
            frame.log_msg(f"{error_msg}")
            wx.MessageBox(error_msg, "Permission Error", wx.OK | wx.ICON_ERROR)

        except Exception as e:
            error_msg = f"Failed to install addon:\n{e}\n\nPlease check the addon file format and try again."
            frame.log_msg(f"{error_msg}")
            wx.MessageBox(error_msg, "Installation Error", wx.OK | wx.ICON_ERROR)
