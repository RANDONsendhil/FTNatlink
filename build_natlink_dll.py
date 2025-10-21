"""
Natlink DLL Build Script
========================

This script helps you get natlink DLL working with Dragon NaturallySpeaking.

What it does:
• Detects existing natlink installations
• Checks Dragon NaturallySpeaking installation
• Attempts to build natlink DLL from source using CMake
• Registers/unregisters DLLs with Windows
• Provides alternative solutions if build fails

Requirements for building:
• CMake (https://cmake.org/)
• Visual Studio or Visual Studio Build Tools
• 32-bit Python (recommended for Dragon compatibility)

Usage:
  python build_natlink_dll.py          # Interactive build process
  python build_natlink_dll.py --status # Show current status
  python build_natlink_dll.py --help   # Show help

For development without DLL:
  python develop_with_fake_runtime.py  # Use fake natlink runtime
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil
import platform


def check_existing_natlink():
    """Check for existing natlink installations"""
    print("🔍 Checking for existing natlink installations...")

    # Check common installation locations
    possible_locations = [
        Path(os.environ.get("PROGRAMFILES", "")) / "Natlink",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Natlink",
        Path(os.environ.get("APPDATA", "")) / "Python" / "natlink",
        Path.home() / "AppData" / "Local" / "Programs" / "natlink",
    ]

    found_installations = []
    for location in possible_locations:
        if location.exists():
            # Look for DLL files
            for dll in location.rglob("*natlink*.dll"):
                print(f"📄 Found existing DLL: {dll}")
                found_installations.append(dll)

    return found_installations


def check_python_architecture():
    """Check if Python is 32-bit or 64-bit"""
    arch = platform.architecture()[0]
    is_64bit = arch == "64bit"
    print(f"🐍 Python architecture: {arch}")

    if is_64bit:
        print("⚠️  Warning: You're using 64-bit Python")
        print(
            "   Dragon NaturallySpeaking typically requires 32-bit Python for natlink"
        )
    else:
        print("✅ Using 32-bit Python (recommended for Dragon)")

    return is_64bit


def check_build_requirements():
    """Check if build requirements are available"""
    print("🔍 Checking build requirements...")

    requirements = {
        "cmake": "cmake --version",
        "Visual Studio": "where cl",  # C++ compiler
        "git": "git --version",
        "Python": "python --version",
    }

    available = {}
    for name, command in requirements.items():
        try:
            result = subprocess.run(
                command.split(), capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                print(f"✅ {name} - Available")
                available[name] = True
            else:
                print(f"❌ {name} - Not found")
                available[name] = False
        except Exception:
            print(f"❌ {name} - Not found")
            available[name] = False

    return available


def find_natlink_source():
    """Find natlink source directories"""
    print("\n🔍 Looking for natlink source...")

    project_root = Path(__file__).parent
    natlink_dirs = [
        project_root / "packages" / "natlink",
        project_root / "packages" / "natlink" / "NatlinkSource",
        project_root / "packages" / "natlink" / "pythonsrc",
    ]

    found_dirs = []
    for dir_path in natlink_dirs:
        if dir_path.exists():
            print(f"📁 Found: {dir_path}")
            found_dirs.append(dir_path)

            # Look for CMakeLists.txt
            cmake_file = dir_path / "CMakeLists.txt"
            if cmake_file.exists():
                print(f"📄 CMakeLists.txt found in {dir_path}")

    return found_dirs


def check_cmake_build():
    """Check if CMake build is possible"""
    print("\n🔍 Checking CMake build setup...")

    project_root = Path(__file__).parent
    cmake_file = project_root / "packages" / "natlink" / "CMakeLists.txt"

    if cmake_file.exists():
        print(f"✅ CMakeLists.txt found: {cmake_file}")

        # Read CMakeLists.txt to understand build
        try:
            with open(cmake_file, "r") as f:
                content = f.read()
                if "natlink" in content.lower():
                    print("✅ CMakeLists.txt appears to be for natlink")
                    return True
        except Exception as e:
            print(f"❌ Error reading CMakeLists.txt: {e}")

    return False


def attempt_cmake_build():
    """Attempt to build natlink using CMake"""
    print("\n🔨 Attempting CMake build...")

    project_root = Path(__file__).parent
    natlink_dir = project_root / "packages" / "natlink"
    build_dir = natlink_dir / "build"

    # Create build directory
    build_dir.mkdir(exist_ok=True)

    print(f"📁 Build directory: {build_dir}")

    # Configure
    print("⚙️  Configuring with CMake...")
    try:
        config_result = subprocess.run(
            [
                "cmake",
                "-S",
                str(natlink_dir),
                "-B",
                str(build_dir),
                "-A",
                "x64",  # 64-bit build
            ],
            capture_output=True,
            text=True,
        )

        print("CMake Configure Output:")
        print(config_result.stdout)
        if config_result.stderr:
            print("CMake Configure Errors:")
            print(config_result.stderr)

        if config_result.returncode == 0:
            print("✅ CMake configuration successful")

            # Build
            print("🔨 Building...")
            build_result = subprocess.run(
                ["cmake", "--build", str(build_dir), "--config", "Release"],
                capture_output=True,
                text=True,
            )

            print("CMake Build Output:")
            print(build_result.stdout)
            if build_result.stderr:
                print("CMake Build Errors:")
                print(build_result.stderr)

            if build_result.returncode == 0:
                print("✅ Build successful!")
                return True
            else:
                print("❌ Build failed")
        else:
            print("❌ CMake configuration failed")

    except Exception as e:
        print(f"❌ CMake build error: {e}")

    return False


def find_built_dll():
    """Find the built natlink DLL"""
    print("\n🔍 Looking for built DLL...")

    project_root = Path(__file__).parent
    search_dirs = [
        project_root / "packages" / "natlink" / "build",
        project_root / "packages" / "natlink" / "build" / "Release",
        project_root / "packages" / "natlink" / "build" / "Debug",
    ]

    dll_patterns = ["*natlink*.dll", "*natlink*.pyd", "_natlink_core*"]

    found_files = []
    for search_dir in search_dirs:
        if search_dir.exists():
            for pattern in dll_patterns:
                for dll_file in search_dir.rglob(pattern):
                    found_files.append(dll_file)
                    print(f"📄 Found: {dll_file}")

    return found_files


def check_dragon_installation():
    """Check for Dragon NaturallySpeaking installation"""
    print("\n🔍 Checking for Dragon NaturallySpeaking...")

    dragon_paths = [
        Path(os.environ.get("PROGRAMFILES", "")) / "Nuance" / "NaturallySpeaking16",
        Path(os.environ.get("PROGRAMFILES(X86)", ""))
        / "Nuance"
        / "NaturallySpeaking16",
        Path(os.environ.get("PROGRAMFILES", "")) / "Dragon",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Dragon",
    ]

    for path in dragon_paths:
        if path.exists():
            print(f"✅ Dragon found: {path}")
            return path

    print("❌ Dragon NaturallySpeaking not found")
    return None


def register_dll(dll_path):
    """Register the natlink DLL"""
    print(f"\n📋 Registering DLL: {dll_path}")

    try:
        # Use regsvr32 to register the DLL
        result = subprocess.run(
            ["regsvr32", "/s", str(dll_path)], capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ DLL registered successfully!")

            # Try to verify registration
            verify_result = subprocess.run(
                ["regsvr32", "/n", "/i", str(dll_path)], capture_output=True, text=True
            )

            return True
        else:
            print(f"❌ Registration failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Registration error: {e}")

    return False


def unregister_dll(dll_path):
    """Unregister the natlink DLL"""
    print(f"\n📋 Unregistering DLL: {dll_path}")

    try:
        result = subprocess.run(
            ["regsvr32", "/u", "/s", str(dll_path)], capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ DLL unregistered successfully!")
            return True
        else:
            print(f"❌ Unregistration failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Unregistration error: {e}")

    return False


def main():
    """Main build process"""
    print("🔨 Natlink DLL Build Script")
    print("=" * 50)
    print("This script helps build the natlink DLL for full Dragon integration\n")

    # Check Python architecture
    is_64bit = check_python_architecture()

    # Check for existing natlink installations
    existing_dlls = check_existing_natlink()
    if existing_dlls:
        print(f"\n✅ Found {len(existing_dlls)} existing natlink DLL(s)")
        choice = (
            input("Do you want to try registering an existing DLL? (y/n): ")
            .lower()
            .strip()
        )
        if choice == "y":
            for dll in existing_dlls:
                if register_dll(dll):
                    print("🎉 Successfully registered existing DLL!")
                    return

    # Check for Dragon installation
    dragon_path = check_dragon_installation()
    if not dragon_path:
        print("⚠️  Dragon NaturallySpeaking not detected")
        print("   The DLL may not work without Dragon installed")

    # Check build requirements
    requirements = check_build_requirements()

    if not all([requirements.get("cmake"), requirements.get("Visual Studio")]):
        print("\n❌ Missing build requirements!")
        print("📋 To build natlink DLL, you need:")
        print("   1. CMake (download from https://cmake.org/)")
        print("   2. Visual Studio with C++ compiler")
        print("   3. Or Visual Studio Build Tools")
        return

    # Find source
    source_dirs = find_natlink_source()
    if not source_dirs:
        print("❌ No natlink source directories found!")
        return

    # Check CMake setup
    if not check_cmake_build():
        print("❌ CMake build not properly configured!")
        return

    print("\n🚀 Ready to build natlink DLL!")
    choice = input("Do you want to proceed with the build? (y/n): ").lower().strip()

    if choice == "y":
        # Attempt build
        if attempt_cmake_build():
            # Look for built DLL
            built_dlls = find_built_dll()

            if built_dlls:
                print(f"\n🎉 Build successful! Found {len(built_dlls)} DLL(s)")

                # Ask about registration
                choice = (
                    input("Do you want to register the DLL with Windows? (y/n): ")
                    .lower()
                    .strip()
                )
                if choice == "y":
                    for dll in built_dlls:
                        register_dll(dll)
            else:
                print("❌ No DLL files found after build")
        else:
            print("❌ Build failed - check error messages above")
    else:
        print("👋 Build cancelled")

    print_alternative_solutions()
    show_status_summary()


def print_alternative_solutions():
    """Print alternative solutions if build fails"""
    print("\n📋 Alternative Solutions:")
    print("=" * 30)
    print("1. 📥 Download pre-built natlink installer:")
    print("   - Visit: https://github.com/dictation-toolbox/natlink/releases")
    print("   - Look for latest natlink installer")
    print()
    print("2. 🔧 Use fake runtime for development:")
    print("   - Run: python develop_with_fake_runtime.py")
    print("   - Good for testing grammars without Dragon")
    print()
    print("3. 🐍 Switch to 32-bit Python:")
    print("   - Dragon typically works better with 32-bit Python")
    print("   - Install Python 3.8-3.11 (32-bit)")
    print()
    print("4. 📚 Manual build instructions:")
    print("   - Check natlink documentation")
    print("   - Visit: https://github.com/dictation-toolbox/natlink")
    print()
    print("5. 🎯 Use Dragon without natlink:")
    print("   - Create Dragon command files (.dvc)")
    print("   - Use Dragon's built-in scripting")


def show_status_summary():
    """Show current project status"""
    print("\n📊 Current Status Summary:")
    print("=" * 30)

    # Check if fake runtime is available
    fake_runtime = Path(__file__).parent / "core" / "fake_natlink_runtime.py"
    if fake_runtime.exists():
        print("✅ Fake natlink runtime available for development")

    # Check if grammars exist
    grammar_dir = Path(__file__).parent / "addons" / "notepad_addon"
    if grammar_dir.exists():
        print("✅ Notepad grammar available")

    # Check dragonfly installation
    try:
        import dragonfly

        print(f"✅ Dragonfly2 installed (version available)")
    except ImportError:
        print("❌ Dragonfly2 not installed")

    print("\n💡 Next Steps:")
    if existing_dlls := check_existing_natlink():
        print("   → Try registering existing natlink DLL")
    else:
        print("   → Build natlink DLL or use alternatives")
        print("   → Test with fake runtime for development")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--status":
            print("🔨 Natlink DLL Status Check")
            print("=" * 50)
            check_python_architecture()
            check_existing_natlink()
            check_dragon_installation()
            check_build_requirements()
            show_status_summary()
        elif arg in ["--help", "-h"]:
            print("🔨 Natlink DLL Build Script")
            print("=" * 50)
            print("Usage:")
            print("  python build_natlink_dll.py          # Interactive build process")
            print("  python build_natlink_dll.py --status # Show status only")
            print("  python build_natlink_dll.py --help   # Show this help")
            print()
            print("This script helps:")
            print("• Check for existing natlink installations")
            print("• Build natlink DLL from source")
            print("• Register DLL with Windows")
            print("• Provide alternative solutions")
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
    else:
        main()
