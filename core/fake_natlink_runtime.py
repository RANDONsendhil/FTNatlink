import types
import sys

# Try to import natlink, or create a mock if Dragon is not available
try:
    import natlink

    print("OK: Real natlink imported successfully")
except (ImportError, AttributeError, NameError) as e:
    # Check if we're allowed to use mock mode
    try:
        from .dragon_config import FORCE_DRAGON_ONLY, ALLOW_MOCK_MODE

        if FORCE_DRAGON_ONLY and not ALLOW_MOCK_MODE:
            print(
                f"❌ ERREUR: Dragon NaturallySpeaking requis mais non disponible ({e})"
            )
            print("❌ Mode factice désactivé - arrêt de l'application")
            raise ImportError(f"Dragon NaturallySpeaking requis: {e}")
    except ImportError:
        # Si dragon_config n'est pas disponible, continuer avec le comportement par défaut
        pass

    # If natlink is not available or fails to initialize, create a minimal mock
    print(f"⚠️ Natlink not available ({e}), using mock implementation")
    natlink = types.ModuleType("natlink")

    # Add essential natlink functions as mocks
    def mock_natConnect(name, func):
        print(f"Mock natConnect: {name}")
        return True

    def mock_natDisconnect():
        print("Mock natDisconnect")
        return True

    natlink.natConnect = mock_natConnect
    natlink.natDisconnect = mock_natDisconnect
    natlink.isNatSpeakRunning = lambda: False

    sys.modules["natlink"] = natlink


class MockGrammar:
    def __init__(self, name="test"):
        self.name = name
        print(f"MockGrammar '{self.name}' initialized")

    def load(self):
        print(f"Grammar '{self.name}' loaded")

    def unload(self):
        print(f"Grammar '{self.name}' unloaded")


# Mock the natlink object - create natlinkmain if it doesn't exist
if not hasattr(natlink, "natlinkmain"):
    natlink.natlinkmain = types.SimpleNamespace(
        GrammarBase=MockGrammar,
        load=None,  # placeholder
    )

# Make natlinkmain available for import
natlinkmain = natlink.natlinkmain
