"""
Addon Packager - Creates .natlink-addon packages
"""

import zipfile
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logHandler import log


def package_addon(addon_folder):
    """Package an addon folder into a .addon-natlink file"""
    addon_path = Path(addon_folder)

    if not addon_path.exists():
        log.error(f"Addon folder not found: {addon_path}")
        return False

    # Read addon.json
    addon_json = addon_path / "addon.json"
    if not addon_json.exists():
        log.error(f"addon.json not found in {addon_path}")
        return False

    with open(addon_json, "r") as f:
        metadata = json.load(f)

    addon_name = metadata.get("name", addon_path.name).replace(" ", "_")
    output_file = addon_path.parent / f"{addon_name}.natlink-addon"

    log.info(f"Packaging addon: {metadata.get('name', 'Unknown')}")
    log.info(f"   Version: {metadata.get('version', '1.0.0')}")

    # Create zip file
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in addon_path.rglob("*"):
            if file.is_file() and not file.name.endswith(".natlink-addon"):
                arcname = file.relative_to(addon_path)
                zipf.write(file, arcname)
                log.info(f"   Added: {arcname}")

    log.info(f"\nPackage created: {output_file}")
    log.info(f"   Size: {output_file.stat().st_size} bytes")
    return True


def main():
    if len(sys.argv) < 2:
        log.info("Usage: python addon_packager.py <addon_folder>")
        log.info("\nExample:")
        log.info("  python addon_packager.py addons/notepad_addon")

        # Show available addons
        addons_dir = Path(__file__).parent.parent / "addons"
        if addons_dir.exists():
            log.info("\n📁 Available addons:")
            for addon in addons_dir.iterdir():
                if addon.is_dir() and not addon.name.startswith("."):
                    addon_json = addon / "addon.json"
                    if addon_json.exists():
                        with open(addon_json, "r") as f:
                            metadata = json.load(f)
                        log.info(
                            f"   • {addon.name} - {metadata.get('name', 'Unknown')}"
                        )
        return

    addon_folder = sys.argv[1]
    success = package_addon(addon_folder)

    if success:
        log.info("\nPackaging complete!")
        log.info("\nTo install:")
        log.info("  1. Use the GUI: File -> Install Addon")
        log.info("  2. Or run: python main.py <package-file>")
    else:
        log.error("\nPackaging failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
