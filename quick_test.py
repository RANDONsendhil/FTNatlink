"""
Quick test script to diagnose FTNatlink without getting stuck
"""

import sys
import os
import natlink
from natlink.grammar import GrammarBase

sys.path.insert(0, os.path.dirname(__file__))

print("=== FTNatlink Quick Test ===")

try:
    print("1. Testing Python architecture...")
    import platform

    print(f"   Architecture: {platform.architecture()[0]}")

    print("2. Testing psutil import...")
    import psutil

    print("   ✅ psutil OK")

    print("3. Testing wxPython import...")
    import wx

    print("   ✅ wxPython OK")

    print("4. Testing natlink import...")
    import natlink

    print("   ✅ natlink imported")

    print("5. Testing natlink functions...")

    if hasattr(natlink, "isNatSpeakRunning"):
        running = natlink.isNatSpeakRunning()
        print(f"   Dragon running: {running}")
    else:
        print("   ❌ isNatSpeakRunning not available")

    if hasattr(natlink, "getMicState"):
        try:
            mic = natlink.getMicState()
            print(f"   Mic state: {mic}")
        except Exception as e:
            print(f"   Mic state error: {e}")
    else:
        print("   ❌ getMicState not available")

    print("6. Testing Dragon processes...")
    dragon_procs = []
    for proc in psutil.process_iter(["name"]):
        if any(
            dragon_name in proc.info["name"].lower()
            for dragon_name in ["natspeak", "dragon", "dragonbar"]
        ):
            dragon_procs.append(proc.info["name"])

    if dragon_procs:
        print(f"   ✅ Dragon processes: {dragon_procs}")
    else:
        print("   ❌ No Dragon processes found")

    print("\n=== Test Complete ===")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
