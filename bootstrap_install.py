#!/usr/bin/env python3
"""
Bootstrap Installation Script for FTNatlink
Handles the chicken-and-egg problem where manage_versions.py needs PyYAML to run
but PyYAML isn't installed in fresh virtual environments.
"""

import sys
import subprocess
import os
from pathlib import Path


def ensure_pyyaml():
    """Ensure PyYAML is installed before running manage_versions.py"""
    try:
        import yaml

        print("✅ PyYAML is already installed")
        return True
    except ImportError:
        print("📦 PyYAML not found, installing...")

        # Install PyYAML first
        cmd = [sys.executable, "-m", "pip", "install", "pyyaml>=6.0"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ PyYAML installed successfully")
            return True
        else:
            print("❌ Failed to install PyYAML")
            print(f"Error: {result.stderr}")
            return False


def fix_pip_if_broken():
    """Fix pip if it's broken (common in fresh venvs)"""
    try:
        # Test if pip works
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ pip is working")
            return True
    except Exception:
        pass

    print("🔧 Fixing pip installation...")

    # Try to repair pip
    try:
        # Run ensurepip to fix pip
        subprocess.run(
            [sys.executable, "-m", "ensurepip", "--upgrade"],
            capture_output=True,
            text=True,
        )

        # Upgrade pip, setuptools, wheel
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
                "setuptools",
                "wheel",
            ],
            capture_output=True,
            text=True,
        )

        print("✅ pip has been repaired")
        return True

    except Exception as e:
        print(f"❌ Failed to repair pip: {e}")
        return False


def run_main_installation():
    """Run the main installation process"""
    print("\n🚀 Running main installation process...")
    print("=" * 60)

    # Import and run manage_versions after PyYAML is available
    try:
        from manage_versions import PackageVersionManager

        manager = PackageVersionManager()
        success = manager.install_all_from_config()

        if success:
            print("\n🎉 Installation completed successfully!")
        else:
            print("\n⚠️ Installation completed with some issues.")

        return success

    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False


def main():
    """Main bootstrap function"""
    print("🔧 FTNatlink Bootstrap Installation")
    print("=" * 50)

    # Check if we're in a virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Warning: Not running in a virtual environment")
        print("   Consider activating your .venv first with: .venv\\Scripts\\activate")

    print(f"🐍 Using Python: {sys.executable}")
    print()

    # Step 1: Fix pip if broken
    if not fix_pip_if_broken():
        print("❌ Cannot proceed without working pip")
        return False

    # Step 2: Ensure PyYAML is installed
    if not ensure_pyyaml():
        print("❌ Cannot proceed without PyYAML")
        return False

    # Step 3: Run main installation
    success = run_main_installation()

    if success:
        print("\n🎯 Bootstrap installation complete!")
        print("\nNext steps:")
        print("  - Check the installation summary")
        print("  - Run tests if available")
        print("  - Start using the installed packages")
    else:
        print("\n❌ Bootstrap installation failed")
        print("\nTroubleshooting:")
        print("  - Check network connectivity")
        print("  - Verify virtual environment is activated")
        print("  - Try recreating the virtual environment")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
