#!/usr/bin/env python
"""
Test microphone monitoring functionality
"""
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_mic_monitoring():
    print("🎤 Test de surveillance du micro Dragon")
    print("=" * 50)
    
    try:
        # Test natlink import and basic functions
        import natlink
        print("✅ Natlink importé avec succès")
        
        # Test Dragon connection
        if hasattr(natlink, 'isNatSpeakRunning'):
            dragon_running = natlink.isNatSpeakRunning()
            print(f"✅ Dragon en cours: {dragon_running}")
        else:
            print("❌ isNatSpeakRunning non disponible")
            return
            
        # Test mic state function
        if hasattr(natlink, 'getMicState'):
            try:
                # Try to connect first
                if hasattr(natlink, 'natConnect'):
                    natlink.natConnect()
                    print("✅ Connexion natlink établie")
                
                mic_state = natlink.getMicState()
                print(f"🎤 État du micro: {mic_state}")
                
                if mic_state == "on":
                    print("✅ Micro Dragon: ON")
                elif mic_state == "off":
                    print("🔇 Micro Dragon: OFF")
                elif mic_state == "sleeping":
                    print("😴 Micro Dragon: SLEEPING")
                else:
                    print(f"❓ Micro Dragon: {mic_state}")
                    
            except Exception as e:
                print(f"❌ Erreur getMicState: {e}")
        else:
            print("❌ getMicState non disponible")
            
    except ImportError as e:
        print(f"❌ Erreur import natlink: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_mic_monitoring()