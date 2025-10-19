import types
import sys

# Try to import natlink, or create a mock
try:
    import natlink
except (ImportError, AttributeError):
    # If natlink is not available, create a minimal mock
    natlink = types.ModuleType('natlink')
    sys.modules['natlink'] = natlink

class MockGrammar:
    def __init__(self, name="test"):
        self.name = name
        print(f"MockGrammar '{self.name}' initialized")

    def load(self):
        print(f"Grammar '{self.name}' loaded")

    def unload(self):
        print(f"Grammar '{self.name}' unloaded")

# Mock the natlink object - create natlinkmain if it doesn't exist
if not hasattr(natlink, 'natlinkmain'):
    natlink.natlinkmain = types.SimpleNamespace(
        GrammarBase=MockGrammar,
        load=None,  # placeholder
    )

# Make natlinkmain available for import
natlinkmain = natlink.natlinkmain