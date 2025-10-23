"""
Inspect natlink module contents
"""

try:
    import natlink

    print("✅ Natlink module imported")

    # List all available functions/attributes
    print("\nAvailable natlink functions:")
    for attr in dir(natlink):
        if not attr.startswith("_"):
            print(f"  - {attr}")

    # Check specific functions we need
    required_functions = [
        "isNatSpeakRunning",
        "getMicState",
        "natConnect",
        "natDisconnect",
    ]
    print("\nRequired function availability:")
    for func in required_functions:
        if hasattr(natlink, func):
            print(f"  ✅ {func}")
        else:
            print(f"  ❌ {func}")

    # Try alternative connection methods
    print("\nTrying alternative connection methods:")

    if hasattr(natlink, "isNatSpeakRunning"):
        try:
            running = natlink.isNatSpeakRunning()
            print(f"  isNatSpeakRunning(): {running}")
        except Exception as e:
            print(f"  isNatSpeakRunning() error: {e}")

    if hasattr(natlink, "getMicState"):
        try:
            mic = natlink.getMicState()
            print(f"  getMicState(): {mic}")
        except Exception as e:
            print(f"  getMicState() error: {e}")

except ImportError as e:
    print(f"❌ Cannot import natlink: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
