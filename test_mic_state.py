#!/usr/bin/env python3
"""
Test script to check Dragon microphone state
"""


def test_mic_state():
    """Test if we can get Dragon microphone state"""
    try:
        import natlink

        print("✅ Natlink imported successfully")

        # Check if Dragon is running
        if hasattr(natlink, "isNatSpeakRunning"):
            running = natlink.isNatSpeakRunning()
            print(f"Dragon running: {running}")
        else:
            print("❌ isNatSpeakRunning not available")
            return

        # Check if we can get mic state
        if hasattr(natlink, "getMicState"):
            try:
                mic_state = natlink.getMicState()
                print(f"Mic state: {mic_state}")
                if mic_state == "on":
                    print("🎤 Microphone is ON")
                elif mic_state == "off":
                    print("🔇 Microphone is OFF")
                elif mic_state == "sleeping":
                    print("😴 Microphone is SLEEPING")
                else:
                    print(f"❓ Unknown mic state: {mic_state}")
            except Exception as e:
                print(f"❌ Error getting mic state: {e}")
        else:
            print("❌ getMicState not available")

    except ImportError as e:
        print(f"❌ Cannot import natlink: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_mic_state()
