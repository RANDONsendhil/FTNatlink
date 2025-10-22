import os
import sys
import importlib.util
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .logHandler import log

GRAMMAR_DIR = Path(__file__).parent.parent / "grammars"
ADDON_DIR = Path(__file__).parent.parent / "addons"
LOADED = {}


def load_grammars():
    """Load all grammars from the grammars folder and addons folder."""
    LOADED.clear()

    # Ensure directories exist
    GRAMMAR_DIR.mkdir(exist_ok=True)

    # Load grammars from grammars/ folder
    for file in GRAMMAR_DIR.glob("*.py"):
        if file.name.startswith("__"):
            continue
        _load_grammar_file(file)

    # Load grammars from grammars/ subdirectories (installed addons)
    for subdir in GRAMMAR_DIR.iterdir():
        if subdir.is_dir():
            for file in subdir.glob("*.py"):
                if file.name.startswith("__"):
                    continue
                _load_grammar_file(file)

    # Load grammars from addons/ folder (development addons)
    if ADDON_DIR.exists():
        for addon_folder in ADDON_DIR.iterdir():
            if addon_folder.is_dir():
                # Check if it has an addon.json
                addon_json = addon_folder / "addon.json"
                if addon_json.exists():
                    # Load all .py files in this addon
                    for file in addon_folder.glob("*.py"):
                        if file.name.startswith("__"):
                            continue
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
    """Unload all grammars."""
    for name, mod in list(LOADED.items()):
        try:
            if hasattr(mod, "grammar"):
                mod.grammar.unload()
            log.info(f"Unloaded: {name}")
        except Exception as e:
            log.error(f"Error unloading {name}: {e}")
    LOADED.clear()


def reload_grammars():
    unload_grammars()
    load_grammars()


def list_grammars():
    """Return list of available grammar names from all sources."""
    grammars = []

    # Ensure directory exists
    GRAMMAR_DIR.mkdir(exist_ok=True)

    # Grammars from grammars/ folder
    for f in GRAMMAR_DIR.glob("*.py"):
        if not f.name.startswith("__"):
            grammars.append(f.stem)

    # Grammars from grammars/ subdirectories (installed addons)
    for subdir in GRAMMAR_DIR.iterdir():
        if subdir.is_dir():
            for f in subdir.glob("*.py"):
                if not f.name.startswith("__"):
                    grammars.append(f.stem)

    # Grammars from addons/ folder (development addons)
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
    """Find grammar file in any of the three locations."""
    if not grammar_name.endswith(".py"):
        grammar_name = f"{grammar_name}.py"

    # Location 1: Direct in grammars/
    grammar_file = GRAMMAR_DIR / grammar_name
    if grammar_file.exists():
        return grammar_file

    # Location 2: In grammars subdirectories (installed addons)
    if GRAMMAR_DIR.exists():
        for subdir in GRAMMAR_DIR.iterdir():
            if subdir.is_dir():
                grammar_file = subdir / grammar_name
                if grammar_file.exists():
                    return grammar_file

    # Location 3: In addons/ folder (development addons)
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

        # Remove from loaded grammars
        del LOADED[grammar_name]
        log.info(f"Successfully unloaded individual grammar: {grammar_name}")
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
