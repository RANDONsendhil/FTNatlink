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

# Import and initialize the notepad grammar
from .notepad_grammar import NotepadGrammar


def load_grammar():
    """Load the notepad grammar"""
    log.info("Loading Notepad Addon...")
    grammar = NotepadGrammar()
    grammar.load()
    return grammar


def main():
    """Main function to run the notepad addon"""
    log.info("📝 Notepad Addon - Voice Commands")
    log.info("=" * 40)
    log.info("Loading notepad voice grammar...")

    # Load the grammar
    grammar = load_grammar()

    log.info("\nNotepad addon loaded successfully!")
    log.info("Available voice commands:")
    for cmd in grammar.commands.keys():
        log.info(f"   - '{cmd}'")

    log.info("\nTesting the grammar...")
    log.info("Simulating 'ouvre bloc note' command:")
    grammar.gotResults(["ouvre", "bloc", "note"], None)

    log.info("\nTo use with Dragon:")
    log.info("1. Make sure Dragon NaturallySpeaking is running")
    log.info("2. Say one of the commands listed above")
    log.info("3. Notepad should open with French text")


if __name__ == "__main__":
    main()
