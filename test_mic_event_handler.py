#!/usr/bin/env python3
"""
Test script for MicEventHandler
"""


def test_mic_event_handler():
    """Test the MicEventHandler implementation"""
    try:
        import natlink

        print("✅ Natlink imported successfully")

        # Test basic functionality first
        if not natlink.isNatSpeakRunning():
            print("❌ Dragon is not running")
            return

        print("✅ Dragon is running")

        # Try to create the MacroSystem
        class TestMicMacroSystem(natlink.MacroSystem):
            def __init__(self):
                print("Creating MacroSystem...")
                super().__init__()
                print("✅ MacroSystem created successfully")

                # Get initial mic state
                try:
                    mic_state = natlink.getMicState()
                    print(f"Initial mic state: {mic_state}")
                except Exception as e:
                    print(f"❌ Error getting initial mic state: {e}")

            def micStateChange(self, newState):
                """Called automatically when Dragon mic state changes"""
                print(f"🎤 Mic state changed to: {newState}")

        # Create the test system
        test_system = TestMicMacroSystem()
        print("✅ MicEventHandler test setup complete")

        # Wait a bit to see if events come in
        import time

        print("Waiting 10 seconds for mic events...")
        time.sleep(10)
        print("Test complete")

    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_mic_event_handler()
