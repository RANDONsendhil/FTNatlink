"""
Configuration pour forcer l'utilisation de Dragon NaturallySpeaking
Ce fichier configure FTNatlink pour fonctionner UNIQUEMENT avec Dragon.
"""

# Configuration principale - MODE DRAGON UNIQUEMENT
FORCE_DRAGON_ONLY = True  # Mode Dragon uniquement - OBLIGATOIRE
ALLOW_MOCK_MODE = False  # Interdit le mode factice
EXIT_ON_DRAGON_FAIL = False  # Ne pas quitter - DEBUG temporaire
REQUIRE_MIC_ON = True  # Surveillance micro ACTIVÉE - Dragon fonctionnel

# Messages d'erreur
DRAGON_NOT_FOUND_MESSAGE = """
❌ ERREUR: Dragon NaturallySpeaking requis

FTNatlink est configuré pour fonctionner UNIQUEMENT avec Dragon NaturallySpeaking.

Problèmes détectés:
- Dragon NaturallySpeaking n'est pas installé ou n'est pas démarré
- Le service Dragon Speech Recognition n'est pas en cours d'exécution
- Natlink n'est pas correctement configuré

Solutions:
1. Démarrer Dragon NaturallySpeaking
2. Vérifier que Dragon fonctionne correctement
3. Installer natlink si nécessaire
4. Utiliser Python 32-bit (Dragon ne supporte que 32-bit)

L'application va maintenant se fermer.
"""

PYTHON_64BIT_ERROR = """
❌ ERREUR: Python 64-bit détecté

Dragon NaturallySpeaking ne fonctionne qu'avec Python 32-bit.

Votre configuration actuelle:
- Python 64-bit (incompatible avec Dragon)

Solutions:
1. Installer Python 32-bit
2. Reconstruire FTNatlink avec Python 32-bit
3. Configurer l'environnement virtuel en 32-bit

L'application va maintenant se fermer.
"""

NATLINK_CONNECTION_ERROR = """
❌ ERREUR: Connexion natlink impossible

Impossible de se connecter à Dragon NaturallySpeaking.

Problèmes possibles:
- Dragon n'est pas démarré
- Natlink n'est pas correctement installé
- Conflit de version Python/Dragon
- Permissions insuffisantes

L'application va maintenant se fermer.
"""

DRAGON_MIC_OFF_ERROR = """
❌ ERREUR: Micro Dragon éteint ou en pause

FTNatlink nécessite que le micro Dragon soit activé pour fonctionner.

État détecté:
- Dragon NaturallySpeaking est démarré ✅
- Micro Dragon est éteint ou en pause ❌

Solutions:
1. Cliquer sur le micro Dragon pour l'activer
2. Dire "Micro on" ou "Wake up"
3. Vérifier les paramètres audio Dragon

FTNatlink va se mettre en pause jusqu'à activation du micro.
"""
