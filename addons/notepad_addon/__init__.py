"""
Notepad Addon Package
Initializes and loads the notepad grammar for voice commands
"""

import sys
from pathlib import Path

# Add project root to path
addon_dir = Path(__file__).parent
project_root = addon_dir.parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
from core.logging_config import get_logger

log = get_logger(__name__)

# Import the global mirror module (the actual grammar)
from . import _global_mirror


def load_grammar():
    """Load the notepad grammar - the actual grammars are loaded by _global_mirror.py"""
    log.info("Loading Notepad Addon...")
    # The grammars are already loaded by importing _global_mirror
    log.info(
        "Notepad grammars loaded: notepad_addon_control and notepad_addon_dictation"
    )
    return True


def main():
    """Main function to run the notepad addon"""
    log.info("📝 Notepad Addon - Voice Commands")
    log.info("=" * 40)
    log.info("Loading notepad voice grammar...")

    # Load the grammar
    load_grammar()

    log.info("\nNotepad addon loaded successfully!")
    log.info("Available voice commands:")
    log.info("   - 'ouvre bloc note' - Open Notepad")
    log.info("   - 'ferme bloc note' - Close Notepad")
    log.info("   - 'sauvegarde' - Save file")
    log.info("   - And many more...")

    log.info("\nTo use with Dragon:")
    log.info("1. Make sure Dragon NaturallySpeaking is running")
    log.info("2. Say one of the commands listed above")
    log.info("3. Notepad should open with French text")


if __name__ == "__main__":
    main()
