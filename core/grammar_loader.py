import os
import sys
import importlib.util
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .logHandler import log

ADDON_DIR = Path(__file__).parent.parent / "addons"
LOADED = {}


def load_grammars():
    """Load all grammars from addons folder only."""
    LOADED.clear()

    # Vérifier Dragon avant le chargement des grammaires
    try:
        from .dragon_checker import verify_dragon_availability
        from .dragon_config import FORCE_DRAGON_ONLY

        if FORCE_DRAGON_ONLY:
            success, message = verify_dragon_availability()
            if not success:
                log.error(
                    "❌ Impossible de charger les grammaires - Dragon NaturallySpeaking requis"
                )
                log.error(message)
                return
            log.info("✅ Dragon vérifié - chargement des grammaires autorisé")
    except ImportError:
        # Si les modules de vérification ne sont pas disponibles, continuer
        log.warning(
            "Modules de vérification Dragon non disponibles - chargement normal"
        )

    # Collect all grammar files from addons only
    grammar_files = []

    # From addons/ folder only
    if ADDON_DIR.exists():
        for addon_folder in ADDON_DIR.iterdir():
            if addon_folder.is_dir():
                addon_json = addon_folder / "addon.json"
                if addon_json.exists():
                    for file in addon_folder.glob("*.py"):
                        if not file.name.startswith("__"):
                            grammar_files.append(file)

    # Load grammars with progress updates
    total_files = len(grammar_files)
    if total_files == 0:
        return

    for i, file in enumerate(grammar_files):
        _load_grammar_file(file)


def _load_grammar_file(file):
    """Load a single grammar file."""
    try:
        spec = importlib.util.spec_from_file_location(file.stem, file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[file.stem] = module
        spec.loader.exec_module(module)
        LOADED[file.stem] = module
        log.info(f"Loaded grammar: {file.stem} ({file.parent.name})")
    except Exception as e:
        log.error(f"Error loading {file.stem}: {e}")


def unload_grammars():
    """Unload all grammars with forced Dragonfly cleanup."""
    log.info("🔄 Déchargement complet de toutes les grammaires...")

    for name, mod in list(LOADED.items()):
        try:
            # Force unload individual grammar using improved method
            unload_individual_grammar(name)
        except Exception as e:
            log.error(f"Error unloading {name}: {e}")

    # Clear the loaded dictionary
    LOADED.clear()
    log.info("✅ Toutes les grammaires déchargées")


def force_unload_all():
    """Emergency unload - forces cleanup of all possible grammar objects."""
    log.info("🚨 DÉCHARGEMENT D'URGENCE - Nettoyage complet")

    # Try to access Dragonfly engine and force cleanup
    try:
        from dragonfly import get_engine

        engine = get_engine()
        if engine:
            # Try to unload all grammars from the engine
            log.info("🧹 Nettoyage moteur Dragonfly...")
    except Exception as e:
        log.warning(f"Impossible d'accéder au moteur Dragonfly: {e}")

    # Standard unload
    unload_grammars()

    log.info("🛑 DÉCHARGEMENT D'URGENCE TERMINÉ")


def reload_grammars():
    unload_grammars()
    load_grammars()


def list_grammars():
    """Return list of available grammar names from addons only."""
    grammars = []

    # Grammars from addons/ folder only
    if ADDON_DIR.exists():
        for addon_folder in ADDON_DIR.iterdir():
            if addon_folder.is_dir():
                addon_json = addon_folder / "addon.json"
                if addon_json.exists():
                    for f in addon_folder.glob("*.py"):
                        if not f.name.startswith("__"):
                            grammars.append(f.stem)

    return sorted(list(set(grammars)))  # Remove duplicates and sort


def find_grammar_file(grammar_name):
    """Find grammar file in addons folder only."""
    if not grammar_name.endswith(".py"):
        grammar_name = f"{grammar_name}.py"

    # Search in addons/ folder only
    if ADDON_DIR.exists():
        for addon_folder in ADDON_DIR.iterdir():
            if addon_folder.is_dir():
                addon_json = addon_folder / "addon.json"
                if addon_json.exists():
                    grammar_file = addon_folder / grammar_name
                    if grammar_file.exists():
                        return grammar_file

    return None


def load_individual_grammar(grammar_name):
    """Load a single grammar by name."""
    try:
        # If already loaded, don't reload
        if grammar_name in LOADED:
            log.info(f"Grammar '{grammar_name}' is already loaded")
            return True

        # Find the grammar file
        grammar_file = find_grammar_file(grammar_name)
        if not grammar_file:
            log.error(f"Grammar file not found: {grammar_name}")
            return False

        # Load the grammar
        success = _load_grammar_file(grammar_file)
        if success:
            log.info(f"Successfully loaded individual grammar: {grammar_name}")
            return True
        else:
            log.error(f"Failed to load individual grammar: {grammar_name}")
            return False

    except Exception as e:
        log.error(f"Error loading individual grammar {grammar_name}: {e}")
        return False


def unload_individual_grammar(grammar_name):
    """Unload a single grammar by name."""
    try:
        if grammar_name not in LOADED:
            log.warning(f"Grammar '{grammar_name}' is not loaded")
            return False

        # Get the loaded module
        mod = LOADED[grammar_name]

        # Force unload from Dragonfly/Dragon if the module has grammars
        try:
            # Look for grammar objects in the module
            if hasattr(mod, "control_grammar"):
                mod.control_grammar.disable()
                mod.control_grammar.unload()
                log.info(f"Déchargé control_grammar de {grammar_name}")

            if hasattr(mod, "dictation_grammar"):
                mod.dictation_grammar.disable()
                mod.dictation_grammar.unload()
                log.info(f"Déchargé dictation_grammar de {grammar_name}")

            # Generic fallback - look for any grammar attribute
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if hasattr(attr, "unload") and hasattr(attr, "disable"):
                    try:
                        attr.disable()
                        attr.unload()
                        log.info(f"Déchargé {attr_name} de {grammar_name}")
                    except:
                        pass  # Ignore errors for non-grammar objects

        except Exception as e:
            log.warning(f"Erreur lors du déchargement forcé de {grammar_name}: {e}")

        # Remove from loaded grammars
        del LOADED[grammar_name]
        log.info(f"✅ Successfully unloaded individual grammar: {grammar_name}")
        return True

    except Exception as e:
        log.error(f"Error unloading individual grammar {grammar_name}: {e}")
        return False


def reload_individual_grammar(grammar_name):
    """Reload a single grammar by name."""
    try:
        # First unload if loaded
        if grammar_name in LOADED:
            unload_individual_grammar(grammar_name)

        # Then load again
        success = load_individual_grammar(grammar_name)
        if success:
            log.info(f"Successfully reloaded individual grammar: {grammar_name}")
            return True
        else:
            log.error(f"Failed to reload individual grammar: {grammar_name}")
            return False

    except Exception as e:
        log.error(f"Error reloading individual grammar {grammar_name}: {e}")
        return False
