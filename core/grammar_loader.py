import os
import sys
import importlib.util
from pathlib import Path
from .logging_config import get_logger

# Setup logging
log = get_logger(__name__)

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
        log.info(f"✅ Loaded grammar: {file.stem} ({file.parent.name})")
    except Exception as e:
        log.error(f"❌ Error loading {file.stem}: {e}")


def unload_grammars():
    """Unload all grammars."""
    for name, mod in list(LOADED.items()):
        try:
            if hasattr(mod, "grammar"):
                mod.grammar.unload()
            log.info(f"🔻 Unloaded: {name}")
        except Exception as e:
            log.error(f"⚠️ Error unloading {name}: {e}")
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
