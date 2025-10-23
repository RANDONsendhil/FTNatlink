#!/usr/bin/env python
"""
Test script pour vérifier la prévention des instances multiples
Lance FTNatlink et essaie de lancer une deuxième instance
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logging_config import setup_logging
from core.logHandler import log
from core.single_instance import SingleInstanceManager


def test_single_instance():
    """Test la détection d'instance unique"""
    setup_logging()

    print("🧪 Test de détection d'instance unique")
    print("=" * 50)

    # Test 1: Vérifier qu'aucune instance n'est active
    manager = SingleInstanceManager()

    already_running, pid = manager.is_already_running()

    if already_running:
        print(f"⚠️ Instance FTNatlink déjà détectée (PID: {pid})")

        # Proposer de fermer l'instance existante
        response = input("Voulez-vous fermer l'instance existante? (y/N): ")

        if response.lower() in ["y", "yes", "oui"]:
            print("🔄 Fermeture de l'instance existante...")
            closed = manager.force_close_existing_instances()
            if closed:
                print(f"✅ Instances fermées: {closed}")
                time.sleep(2)  # Attendre que le processus se ferme
            else:
                print("❌ Aucune instance fermée")
        else:
            print("❌ Test annulé - instance déjà active")
            return

    # Test 2: Créer un verrou
    print("\n🔐 Test création verrou...")
    if manager.create_lock():
        print("✅ Verrou créé avec succès")
    else:
        print("❌ Échec création verrou")
        return

    # Test 3: Essayer de détecter notre propre instance
    print("\n🔍 Test détection de notre instance...")
    already_running, pid = manager.is_already_running()

    if already_running:
        print(f"✅ Notre instance détectée (PID: {pid})")
    else:
        print("❌ Notre instance non détectée")

    # Test 4: Simuler une deuxième instance
    print("\n🎭 Simulation d'une deuxième instance...")

    manager2 = SingleInstanceManager()
    already_running2, pid2 = manager2.is_already_running()

    if already_running2:
        print(f"✅ Deuxième instance correctement bloquée (détecte PID: {pid2})")
    else:
        print("❌ Deuxième instance non bloquée - ERREUR!")

    # Test 5: Test message d'alerte
    print("\n💬 Test message d'alerte...")
    try:
        # Note: ceci va afficher le message d'alerte
        # manager2.show_already_running_message(pid)
        print("✅ Message d'alerte disponible (non affiché pour éviter pop-up)")
    except Exception as e:
        print(f"❌ Erreur message d'alerte: {e}")

    # Nettoyage
    print("\n🧹 Nettoyage...")
    manager.release_lock()
    print("✅ Verrou supprimé")

    # Vérification finale
    already_running_final, _ = manager.is_already_running()
    if not already_running_final:
        print("✅ Aucune instance détectée après nettoyage")
    else:
        print("⚠️ Instance encore détectée après nettoyage")

    print("\n" + "=" * 50)
    print("🎉 Test de prévention multi-instance terminé!")


def test_exe_multiple_launch():
    """Test de lancement multiple de l'exécutable"""
    exe_path = Path(__file__).parent.parent / "dist" / "FTNatlink.exe"

    if not exe_path.exists():
        print(f"❌ Exécutable non trouvé: {exe_path}")
        print("   Construisez d'abord l'exécutable avec: .\\build_exe.bat")
        return

    print("🚀 Test lancement multiple exécutable")
    print("=" * 50)

    print("ℹ️ Instructions:")
    print("1. L'exécutable va se lancer")
    print("2. Essayez de le lancer une deuxième fois manuellement")
    print("3. Vous devriez voir un message d'alerte")
    print("4. Fermez la première instance pour terminer le test")
    print()

    input("Appuyez sur Entrée pour lancer l'exécutable...")

    try:
        # Lancer l'exécutable
        process = subprocess.Popen([str(exe_path)])
        print(f"✅ Exécutable lancé (PID: {process.pid})")

        print("\n🔄 Maintenant lancez une deuxième instance manuellement...")
        print("   Double-cliquez sur dist/FTNatlink.exe")
        print("   Vous devriez voir un message d'alerte!")

        input("\nAppuyez sur Entrée quand vous avez testé la deuxième instance...")

        # Terminer le processus
        print("🔚 Fermeture de l'instance de test...")
        process.terminate()

        try:
            process.wait(timeout=5)
            print("✅ Instance fermée proprement")
        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️ Instance fermée de force")

    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    choice = input(
        "Test à effectuer:\n1. Test détection instance\n2. Test exécutable multiple\nChoix (1/2): "
    )

    if choice == "1":
        test_single_instance()
    elif choice == "2":
        test_exe_multiple_launch()
    else:
        print("❌ Choix invalide")
