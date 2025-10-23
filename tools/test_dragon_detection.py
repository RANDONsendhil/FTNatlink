#!/usr/bin/env python
"""
Script de test pour la vérification Dragon NaturallySpeaking
Teste si FTNatlink peut détecter Dragon correctement
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logging_config import setup_logging
from core.logHandler import log
from core.dragon_checker import (
    verify_dragon_availability,
    check_python_architecture,
    check_dragon_process,
    check_natlink_availability,
    check_dragon_mic_state,
    enforce_dragon_requirement,
    DragonVerificationError,
)
from core.dragon_config import (
    FORCE_DRAGON_ONLY,
    ALLOW_MOCK_MODE,
    EXIT_ON_DRAGON_FAIL,
    REQUIRE_MIC_ON,
)


def main():
    """Test de vérification Dragon"""
    setup_logging()

    print("🔍 Test de vérification Dragon NaturallySpeaking")
    print("=" * 50)

    # Afficher la configuration
    print(f"Configuration actuelle:")
    print(f"- FORCE_DRAGON_ONLY: {FORCE_DRAGON_ONLY}")
    print(f"- ALLOW_MOCK_MODE: {ALLOW_MOCK_MODE}")
    print(f"- EXIT_ON_DRAGON_FAIL: {EXIT_ON_DRAGON_FAIL}")
    print(f"- REQUIRE_MIC_ON: {REQUIRE_MIC_ON}")
    print()

    # Test de l'architecture Python
    print("1. Test architecture Python:")
    python_ok, python_msg = check_python_architecture()
    status = "✅" if python_ok else "❌"
    print(f"   {status} {python_msg}")
    print()

    # Test des processus Dragon
    print("2. Test processus Dragon:")
    process_ok, process_msg = check_dragon_process()
    status = "✅" if process_ok else "❌"
    print(f"   {status} {process_msg}")
    print()

    # Test natlink
    print("3. Test natlink:")
    natlink_ok, natlink_msg = check_natlink_availability()
    status = "✅" if natlink_ok else "❌"
    print(f"   {status} {natlink_msg}")
    print()

    # Test micro Dragon (si requis)
    if REQUIRE_MIC_ON:
        print("4. Test micro Dragon:")
        mic_ok, mic_msg = check_dragon_mic_state()
        status = "✅" if mic_ok else "❌"
        print(f"   {status} {mic_msg}")
        print()

    # Test de vérification complète
    print(f"{'5' if REQUIRE_MIC_ON else '4'}. Vérification complète:")
    success, message = verify_dragon_availability()
    status = "✅" if success else "❌"
    print(
        f"   {status} Dragon NaturallySpeaking: {'DISPONIBLE' if success else 'NON DISPONIBLE'}"
    )
    if not success:
        print(f"   Détails: {message[:100]}...")
    print()

    # Test de l'enforcement
    print("5. Test enforcement (selon configuration):")
    try:
        result = enforce_dragon_requirement()
        if result:
            print("   ✅ Enforcement réussi - application peut continuer")
        else:
            print("   ⚠️ Enforcement échoué mais application peut continuer")
    except DragonVerificationError as e:
        print("   ❌ Enforcement échoué - application doit s'arrêter")
        print(f"   Erreur: {str(e)[:100]}...")
    print()

    # Résumé
    print("=" * 50)
    if success:
        print("🎉 RÉSULTAT: Dragon NaturallySpeaking est prêt!")
        print("   FTNatlink peut fonctionner en mode Dragon réel")
    else:
        print("❌ RÉSULTAT: Dragon NaturallySpeaking n'est pas disponible")
        if FORCE_DRAGON_ONLY:
            print("   FTNatlink ne peut PAS démarrer (mode Dragon uniquement)")
        else:
            print("   FTNatlink peut démarrer en mode factice")


if __name__ == "__main__":
    main()
