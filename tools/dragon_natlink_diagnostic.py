"""
Dragon/Natlink Diagnostic Script
Checks Dragon and natlink status without importing problematic modules
"""

import os
import sys
import winreg
import subprocess
from pathlib import Path


def check_dragon_processes():
    """Check if Dragon processes are running"""
    print("🔍 Checking Dragon processes...")
    try:
        result = subprocess.run(
            ["tasklist", "/fi", "imagename eq natspeak.exe"],
            capture_output=True,
            text=True,
        )
        if "natspeak.exe" in result.stdout:
            print("✅ Dragon (natspeak.exe) is running")
            return True
        else:
            print("❌ Dragon (natspeak.exe) is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Dragon processes: {e}")
        return False


def check_natlink_registry():
    """Check if natlink DLL is registered"""
    print("\n🔍 Checking natlink registry...")
    clsid = "{dd990001-bb89-11d2-b031-0060088dc929}"
    subkeys = [
        f"WOW6432Node\\CLSID\\{clsid}\\InprocServer32",
        f"CLSID\\{clsid}\\InprocServer32",
    ]

    for subkey in subkeys:
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
            sk = winreg.OpenKey(reg, subkey)
            dll_path = winreg.QueryValue(sk, None)
            print(f"✅ Natlink DLL registered at: {dll_path}")

            # Check if DLL file exists
            if os.path.exists(dll_path):
                print(f"✅ DLL file exists: {dll_path}")
            else:
                print(f"❌ DLL file missing: {dll_path}")
            return dll_path
        except Exception as e:
            print(f"❌ Registry key not found: {subkey}")

    print("❌ Natlink DLL not registered in registry")
    return None


def check_dragon_installation():
    """Check Dragon installation directory"""
    print("\n🔍 Checking Dragon installation...")
    try:
        # Check common Dragon installation paths
        possible_paths = [
            "C:\\Program Files (x86)\\Nuance\\NaturallySpeaking16",
            "C:\\Program Files (x86)\\Nuance\\NaturallySpeaking15",
            "C:\\Program Files\\Nuance\\NaturallySpeaking16",
            "C:\\Program Files\\Nuance\\NaturallySpeaking15",
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Dragon found at: {path}")
                return path

        print("❌ Dragon installation directory not found")
        return None
    except Exception as e:
        print(f"❌ Error checking Dragon installation: {e}")
        return None


def check_natlink_files():
    """Check for natlink DLL files in project"""
    print("\n🔍 Checking natlink DLL files in project...")
    project_root = Path(__file__).parent

    # Look for natlink DLL files
    dll_patterns = ["*natlink*.dll", "*natlink*.pyd", "_natlink_core*"]
    found_files = []

    for pattern in dll_patterns:
        for dll_file in project_root.rglob(pattern):
            found_files.append(dll_file)
            print(f"📁 Found: {dll_file}")

    if not found_files:
        print("❌ No natlink DLL/PYD files found in project")

    return found_files


def test_natlinkcore_only():
    """Test natlinkcore without natlink"""
    print("\n🔍 Testing natlinkcore functionality...")
    try:
        import natlinkcore

        print("✅ natlinkcore imports successfully")

        # Check natlinkcore version and location
        print(f"📍 Location: {natlinkcore.__file__}")
        if hasattr(natlinkcore, "__version__"):
            print(f"📋 Version: {natlinkcore.__version__}")

        return True
    except Exception as e:
        print(f"❌ natlinkcore import failed: {e}")
        return False


def main():
    """Main diagnostic function"""
    print("🔍 Dragon/Natlink Diagnostic Report")
    print("=" * 50)

    dragon_running = check_dragon_processes()
    natlink_dll = check_natlink_registry()
    dragon_path = check_dragon_installation()
    natlink_files = check_natlink_files()
    natlinkcore_ok = test_natlinkcore_only()

    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"Dragon Running: {'✅' if dragon_running else '❌'}")
    print(f"Natlink DLL Registered: {'✅' if natlink_dll else '❌'}")
    print(f"Dragon Installed: {'✅' if dragon_path else '❌'}")
    print(f"Natlink Files Found: {'✅' if natlink_files else '❌'}")
    print(f"Natlinkcore Working: {'✅' if natlinkcore_ok else '❌'}")

    print("\n🔧 NEXT STEPS:")
    if not natlink_dll and dragon_running:
        print("1. Natlink needs to be installed/registered with Dragon")
        print("2. Look for natlink installer or registration script")
        print("3. May need to run 'regsvr32' on the natlink DLL")
    elif not dragon_running:
        print("1. Start Dragon NaturallySpeaking")
        print("2. Ensure Dragon is properly configured")

    if natlinkcore_ok:
        print("3. Consider using natlinkcore directly for basic functionality")


if __name__ == "__main__":
    main()
