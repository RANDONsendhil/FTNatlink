"""
Addon Packager - Creates .addon-natlink packages
"""

import zipfile
import json
from pathlib import Path
import sys

def package_addon(addon_folder):
    """Package an addon folder into a .addon-natlink file"""
    addon_path = Path(addon_folder)
    
    if not addon_path.exists():
        print(f"❌ Addon folder not found: {addon_path}")
        return False
    
    # Read addon.json
    addon_json = addon_path / "addon.json"
    if not addon_json.exists():
        print(f"❌ addon.json not found in {addon_path}")
        return False
    
    with open(addon_json, 'r') as f:
        metadata = json.load(f)
    
    addon_name = metadata.get('name', addon_path.name).replace(' ', '_')
    output_file = addon_path.parent / f"{addon_name}.addon-natlink"
    
    print(f"📦 Packaging addon: {metadata.get('name', 'Unknown')}")
    print(f"   Version: {metadata.get('version', '1.0.0')}")
    
    # Create zip file
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in addon_path.rglob('*'):
            if file.is_file() and not file.name.endswith('.addon-natlink'):
                arcname = file.relative_to(addon_path)
                zipf.write(file, arcname)
                print(f"   ✅ Added: {arcname}")
    
    print(f"\n🎉 Package created: {output_file}")
    print(f"   Size: {output_file.stat().st_size} bytes")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python addon_packager.py <addon_folder>")
        print("\nExample:")
        print("  python addon_packager.py addons/notepad_addon")
        
        # Show available addons
        addons_dir = Path(__file__).parent.parent / "addons"
        if addons_dir.exists():
            print("\n📁 Available addons:")
            for addon in addons_dir.iterdir():
                if addon.is_dir() and not addon.name.startswith('.'):
                    addon_json = addon / "addon.json"
                    if addon_json.exists():
                        with open(addon_json, 'r') as f:
                            metadata = json.load(f)
                        print(f"   • {addon.name} - {metadata.get('name', 'Unknown')}")
        return
    
    addon_folder = sys.argv[1]
    success = package_addon(addon_folder)
    
    if success:
        print("\n✅ Packaging complete!")
        print("\nTo install:")
        print("  1. Use the GUI: File -> Install Addon")
        print("  2. Or run: python main.py <package-file>")
    else:
        print("\n❌ Packaging failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
