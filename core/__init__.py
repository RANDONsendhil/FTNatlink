"""
Core Module - Core functionality for FTNatlink
Contains grammar loading, natlink runtime mocking, and test utilities
"""

from .grammar_loader import (
    load_grammars,
    list_grammars,
    unload_grammars,
    reload_grammars,
    LOADED
)
from .fake_natlink_runtime import natlinkmain, MockGrammar

__all__ = [
    'load_grammars',
    'list_grammars',
    'unload_grammars',
    'reload_grammars',
    'LOADED',
    'natlinkmain',
    'MockGrammar'
]
